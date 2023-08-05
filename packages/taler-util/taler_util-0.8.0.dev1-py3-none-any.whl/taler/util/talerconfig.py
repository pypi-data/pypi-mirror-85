# (C) 2016, 2019 Taler Systems SA
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3 of the License, or (at your option) any later
#  version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free
#  Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA  02110-1301  USA
#
# @author Florian Dold
# @author Marcello Stanisci
# @brief Parse GNUnet-style configurations in pure Python

import logging
import collections
import os
import weakref
import sys
import re
from typing import Callable, Any

LOGGER = logging.getLogger(__name__)

__all__ = ["TalerConfig"]

TALER_DATADIR = None

try:
    # not clear if this is a good idea ...
    from talerpaths import TALER_DATADIR as t

    TALER_DATADIR = t
except ImportError:
    pass

##
# Exception class for a any configuration error.
class ConfigurationError(Exception):
    pass


##
# Exception class for malformed strings having with parameter
# expansion.
class ExpansionSyntaxError(Exception):
    pass


##
# Do shell-style parameter expansion.
# Supported syntax:
#  - ${X}
#  - ${X:-Y}
#  - $X
#
# @param var entire config value that might contain a parameter
#        to expand.
# @param getter function that is in charge of returning _some_
#        value to be used in place of the parameter to expand.
#        Typically, the replacement is searched first under the
#        PATHS section of the current configuration, or (if not
#        found) in the environment.
#
# @return the expanded config value.
def expand(var: str, getter: Callable[[str], str]) -> str:
    pos = 0
    result = ""
    while pos != -1:
        start = var.find("$", pos)
        if start == -1:
            break
        if var[start:].startswith("${"):
            balance = 1
            end = start + 2
            while balance > 0 and end < len(var):
                balance += {"{": 1, "}": -1}.get(var[end], 0)
                end += 1
            if balance != 0:
                raise ExpansionSyntaxError("unbalanced parentheses")
            piece = var[start + 2 : end - 1]
            if piece.find(":-") > 0:
                varname, alt = piece.split(":-", 1)
                replace = getter(varname)
                if replace is None:
                    replace = expand(alt, getter)
            else:
                varname = piece
                replace = getter(varname)
                if replace is None:
                    replace = var[start:end]
        else:
            end = start + 2
            while end < len(var) and var[start + 1 : end + 1].isalnum():
                end += 1
            varname = var[start + 1 : end]
            replace = getter(varname)
            if replace is None:
                replace = var[start:end]
        result = result + replace
        pos = end

    return result + var[pos:]

##
# A configuration entry.
class Entry:

    ##
    # Init constructor.
    #
    # @param self the object itself.
    # @param config reference to a configuration object - FIXME
    #        define "configuration object".
    # @param section name of the config section where this entry
    #        got defined.
    # @param option name of the config option associated with this
    #        entry.
    # @param kwargs keyword arguments that hold the value / filename
    #        / line number of this current option.
    def __init__(self, config, section: str, option: str, **kwargs) -> None:
        self.value = kwargs.get("value")
        self.filename = kwargs.get("filename")
        self.lineno = kwargs.get("lineno")
        self.section = section
        self.option = option
        self.config = weakref.ref(config)

    ##
    # XML representation of this entry.
    #
    # @param self the object itself.
    # @return XML string holding all the relevant information
    #         for this entry.
    def __repr__(self) -> str:
        return "<Entry section=%s, option=%s, value=%s>" % (
            self.section,
            self.option,
            repr(self.value),
        )

    ##
    # Return the value for this entry, as is.
    #
    # @param self the object itself.
    # @return the config value.
    def __str__(self) -> Any:
        return self.value

    ##
    # Return entry value, accepting defaults.
    #
    # @param self the object itself
    # @param default default value to return if none was found.
    # @param required indicate whether the value was required or not.
    #        If the value was required, but was not found, an exception
    #        is found.
    # @param warn if True, outputs a warning message if the value was
    #        not found -- regardless of it being required or not.
    # @return the value, or the given @a default, if not found.
    def value_string(self, default=None, required=False, warn=False) -> str:
        if required and self.value is None:
            print("Missing required option '%s' in section '%s'"
                % (self.option.upper(), self.section.upper()))
            sys.exit(1)

        if self.value is None:
            if warn:
                if default is not None:
                    LOGGER.warning(
                        "Configuration is missing option '%s' in section '%s',\
                                   falling back to '%s'",
                        self.option,
                        self.section,
                        default,
                    )
                else:
                    LOGGER.warning(
                        "Configuration ** is missing option '%s' in section '%s'",
                        self.option.upper(),
                        self.section.upper(),
                    )
            return default
        return self.value

    ##
    # Return entry value as a _int_.  Raise exception if the
    # value is not convertible to a integer.
    #
    # @param self the object itself
    # @param default currently ignored.
    # @param required currently ignored.
    # @param warn currently ignored.
    # @return the value, or the given @a default, if not found.
    def value_int(self, default=None, required=False, warn=False) -> int:
        value = self.value_string(default, required, warn)
        if value is None:
            return None
        try:
            return int(value)
        except ValueError:
            print(
                "Expected number for option '%s' in section '%s'"
                % (self.option.upper(), self.section.upper())
            )
            sys.exit(1)

    ##
    # Fetch value to substitute to expansion variables.
    #
    # @param self the object itself.
    # @param key the value's name to lookup.
    # @return the value, if found, None otherwise.
    def _getsubst(self, key: str) -> Any:
        value = self.config()["paths"][key].value
        if value is not None:
            return value
        value = os.environ.get(key)
        if value is not None:
            return value
        return None

    ##
    # Fetch the config value that should be a filename,
    # taking care of invoking the variable-expansion logic first.
    #
    # @param self the object itself.
    # @param default currently ignored.
    # @param required currently ignored.
    # @param warn currently ignored.
    # @return the (expanded) filename.
    def value_filename(self, default=None, required=False, warn=False) -> str:
        value = self.value_string(default, required, warn)
        if value is None:
            return None
        return expand(value, self._getsubst)

    ##
    # Give the filename and line number of this config entry.
    #
    # @param self this object.
    # @return <filename>:<linenumber>, or "<unknown>" if one
    #         is not known.
    def location(self) -> str:
        if self.filename is None or self.lineno is None:
            return "<unknown>"
        return "%s:%s" % (self.filename, self.lineno)


##
# Represent a section by inheriting from 'defaultdict'.
class OptionDict(collections.defaultdict):

    ##
    # Init constructor.
    #
    # @param self the object itself
    # @param config the "config" object -- typically a @a TalerConfig instance.
    # @param section_name the section name to assign to this object.
    def __init__(self, config, section_name: str) -> None:
        self.config = weakref.ref(config)
        self.section_name = section_name
        super().__init__()

    ##
    # Logic to run when a non-existent key is dereferenced.
    # Just create and return a empty config @a Entry.  Note
    # that the freshly created entry will nonetheless put
    # under the accessed key (that *does* become existent
    # afterwards).
    #
    # @param self the object itself.
    # @param key the key attempted to be accessed.
    # @return the no-value entry.
    def __missing__(self, key: str) -> Entry:
        entry = Entry(self.config(), self.section_name, key)
        self[key] = entry
        return entry

    ##
    # Attempt to fetch one value from the object.
    #
    # @param self the object itself.
    # @param chunk the key (?) that is tried to access.
    # @return the object, if it exists, or a freshly created
    #         (empty) one, if it doesn't exist.
    def __getitem__(self, chunk: str) -> Entry:
        return super().__getitem__(chunk.lower())

    ##
    # Set one value into the object.
    #
    # @param self the object itself.
    # @param chunk key under which the value is going to be set.
    # @param value value to set the @a chunk to.
    def __setitem__(self, chunk: str, value: Entry) -> None:
        super().__setitem__(chunk.lower(), value)


##
# Collection of all the (@a OptionDict) sections.
class SectionDict(collections.defaultdict):

    ##
    # Automatically invoked when a missing section is
    # dereferenced.  It creates the missing - empty - section.
    #
    # @param self the object itself.
    # @param key the dereferenced section name.
    # @return the freshly created section.
    def __missing__(self, key):
        value = OptionDict(self, key)
        self[key] = value
        return value

    ##
    # Attempt to retrieve a section.
    #
    # @param self the object itself.
    # @param chunk the section name.
    def __getitem__(self, chunk: str) -> OptionDict:
        return super().__getitem__(chunk.lower())

    ##
    # Set a section.
    #
    # @param self the object itself.
    # @param chunk the section name to set.
    # @param value the value to set under that @a chunk.
    def __setitem__(self, chunk: str, value: OptionDict) -> None:
        super().__setitem__(chunk.lower(), value)


##
# One loaded taler configuration, including base configuration
# files and included files.
class TalerConfig:

    ##
    # Init constructor..
    #
    # @param self the object itself.
    def __init__(self) -> None:
        self.sections = SectionDict()  # just plain dict

    ##
    # Load a configuration file, instantiating a config object.
    #
    # @param filename the filename where to load the configuration
    #        from.  If None, it defaults "taler.conf".
    # @param load_defaults if True, then defaults values are loaded
    #        (from canonical directories like "<prefix>/share/config.d/taler/")
    #        before the actual configuration file.  This latter then
    #        can override some/all the defaults.
    # @return the config object.
    @staticmethod
    def from_file(filename=None, load_defaults=True):
        cfg = TalerConfig()
        if filename is None:
            xdg = os.environ.get("XDG_CONFIG_HOME")
            if xdg:
                filename = os.path.join(xdg, "taler.conf")
            else:
                filename = os.path.expanduser("~/.config/taler.conf")
            logging.info("Loading default config: (%s)" % filename)
        if load_defaults:
            cfg.load_defaults()
        cfg.load_file(os.path.expanduser(filename))
        return cfg

    ##
    # Get a string value from the config.
    #
    # @param self the config object itself.
    # @param section the section to fetch the value from.
    # @param option the value's option name.
    # @param kwargs dict argument with instructions about
    #        the value retrieval logic.
    # @return the wanted string (or a default / exception if
    #         a error occurs).
    def value_string(self, section, option, **kwargs) -> str:
        return self.sections[section][option].value_string(
            kwargs.get("default"), kwargs.get("required"), kwargs.get("warn")
        )

    ##
    # Get a value from the config that should be a filename.
    # The variable expansion for the path's components is internally managed.
    #
    # @param self the config object itself.
    # @param section the section to fetch the value from.
    # @param option the value's option name.
    # @param kwargs dict argument with instructions about
    #        the value retrieval logic.
    # @return the wanted filename (or a default / exception if
    #         a error occurs).
    def value_filename(self, section, option, **kwargs) -> str:
        return self.sections[section][option].value_filename(
            kwargs.get("default"), kwargs.get("required"), kwargs.get("warn")
        )

    ##
    # Get a integer value from the config.
    #
    # @param self the config object itself.
    # @param section the section to fetch the value from.
    # @param option the value's option name.
    # @param kwargs dict argument with instructions about
    #        the value retrieval logic.
    # @return the wanted integer (or a default / exception if
    #         a error occurs).
    def value_int(self, section, option, **kwargs) -> int:
        return self.sections[section][option].value_int(
            kwargs.get("default"), kwargs.get("required"), kwargs.get("warn")
        )

    ##
    # Load default values from canonical locations.
    #
    # @param self the object itself.
    def load_defaults(self) -> None:
        base_dir = os.environ.get("TALER_BASE_CONFIG")
        if base_dir:
            self.load_dir(base_dir)
            return
        prefix = os.environ.get("TALER_PREFIX")
        if prefix:
            tmp = os.path.split(os.path.normpath(prefix))
            if re.match("lib", tmp[1]):
                prefix = tmp[0]
            self.load_dir(os.path.join(prefix, "share/taler/config.d"))
            return
        if TALER_DATADIR:
            self.load_dir(os.path.join(TALER_DATADIR, "share/taler/config.d"))
            return
        LOGGER.warning("no base directory found")

    ##
    # Load configuration from environment variable
    # TALER_CONFIG_FILE or from default location if the
    # variable is not set.
    #
    # @param args currently unused.
    # @param kwargs kwargs for subroutine @a from_file.
    # @return freshly instantiated config object.
    @staticmethod
    def from_env(*args, **kwargs):
        filename = os.environ.get("TALER_CONFIG_FILE")
        return TalerConfig.from_file(filename, *args, **kwargs)

    ##
    # Load config values from _each_ file found in a directory.
    #
    # @param self the object itself.
    # @param dirname the directory to crawl in the look for config files.
    def load_dir(self, dirname) -> None:
        try:
            files = os.listdir(dirname)
        except FileNotFoundError:
            LOGGER.warning("can't read config directory '%s'", dirname)
            return
        for file in files:
            if not file.endswith(".conf"):
                continue
            self.load_file(os.path.join(dirname, file))

    ##
    # Load config values from a file.
    #
    # @param filename config file to take the values from.
    def load_file(self, filename) -> None:
        sections = self.sections
        try:
            with open(filename, "r") as file:
                lineno = 0
                current_section = None
                for line in file:
                    lineno += 1
                    line = line.strip()
                    if line == "":
                        # empty line
                        continue
                    if line.startswith("#"):
                        # comment
                        continue
                    if line.startswith("@INLINE@"):
                        pair = line.split()
                        if 2 != len(pair):
                            LOGGER.error(
                                "invalid inlined config filename given ('%s')" % line
                            )
                            continue
                        if pair[1].startswith("/"):
                            self.load_file(pair[1])
                        else:
                            self.load_file(
                                os.path.join(os.path.dirname(filename), pair[1])
                            )
                        continue
                    if line.startswith("["):
                        if not line.endswith("]"):
                            LOGGER.error(
                                "invalid section header in line %s: %s",
                                lineno,
                                repr(line),
                            )
                        section_name = line.strip("[]").strip().strip('"')
                        current_section = section_name
                        continue
                    if current_section is None:
                        LOGGER.error(
                            "option outside of section in line %s: %s",
                            lineno,
                            repr(line),
                        )
                        continue
                    pair = line.split("=", 1)
                    if len(pair) != 2:
                        LOGGER.error(
                            "invalid option in line %s: %s", lineno, repr(line)
                        )
                    key = pair[0].strip()
                    value = pair[1].strip()
                    if value.startswith('"'):
                        value = value[1:]
                        if not value.endswith('"'):
                            LOGGER.error(
                                "mismatched quotes in line %s: %s", lineno, repr(line)
                            )
                        else:
                            value = value[:-1]
                    entry = Entry(
                        self.sections,
                        current_section,
                        key,
                        value=value,
                        filename=filename,
                        lineno=lineno,
                    )
                    sections[current_section][key] = entry
        except FileNotFoundError:
            LOGGER.error("Configuration file (%s) not found", filename)
            sys.exit(3)

    ##
    # Dump the textual representation of a config object.
    #
    # Format:
    #
    # [section]
    # option = value # FIXME (what is location?)
    #
    # @param self the object itself, that will be dumped.
    def dump(self) -> None:
        for kv_section in list(self.sections.items()):
            print("[%s]" % (kv_section[1].section_name,))
            for kv_option in list(kv_section[1].items()):
                print(
                    "%s = %s # %s"
                    % (kv_option[1].option, kv_option[1].value, kv_option[1].location())
                )

    ##
    # Return a whole section from this object.
    #
    # @param self the object itself.
    # @param chunk name of the section to return.
    # @return the section - note that if the section is
    #         not found, a empty one will created on the fly,
    #         then set under 'chunk', and returned.
    def __getitem__(self, chunk: str) -> OptionDict:
        if isinstance(chunk, str):
            return self.sections[chunk]
        raise TypeError("index must be string")


if __name__ == "__main__":
    import argparse

    PARSER = argparse.ArgumentParser()
    PARSER.add_argument(
        "--section", "-s", dest="section", default=None, metavar="SECTION"
    )
    PARSER.add_argument("--option", "-o", dest="option", default=None, metavar="OPTION")
    PARSER.add_argument("--config", "-c", dest="config", default=None, metavar="FILE")
    PARSER.add_argument(
        "--filename", "-f", dest="expand_filename", default=False, action="store_true"
    )
    ARGS = PARSER.parse_args()

    TC = TalerConfig.from_file(ARGS.config)

    if ARGS.section is not None and ARGS.option is not None:
        if ARGS.expand_filename:
            X = TC.value_filename(ARGS.section, ARGS.option)
        else:
            X = TC.value_string(ARGS.section, ARGS.option)
        if X is not None:
            print(X)
    else:
        TC.dump()
