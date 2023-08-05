# This file is part of TALER
# (C) 2014, 2015, 2016, 2019 Taler Systems SA
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
# @author Marcello Stanisci
# @brief Implementation of the GNUnet logging logic.
#
#!/usr/bin/env python3

# GNUNET_FORCE_LOG format [component];[file];[function];[from line [to line]];loglevel

import os
import re
import logging
import datetime
import inspect


##
# Represent a definition for one logging action.
class LogDefinition:

    ##
    # Init constructor.
    #
    # @param self the object itself.
    # @param component which component this definition is going to affect.
    # @param filename which filename this definition is going to affect.
    # @param function which function this definition is going to affect.
    # @param line_interval which line_interval this definition is going to affect.
    # @param loglevel which loglevel is accepted.
    # @param forced does this definition come from GNUNET_FORCE_LOG?
    def __init__(self, component, filename, function, line_interval, loglevel, forced):
        self.forced = forced
        self.component = ".*" if "" == component else component
        self.filename = ".*" if "" == filename else filename
        self.function = ".*" if "" == function else function
        self.line_interval = self.__parse_line_interval(line_interval)

        # string here
        self.loglevel = loglevel

    ##
    # Parse the @a line_interval from a logging definition.
    #
    # @param self the object itself.
    # @param line_interval the line interval value as it comes
    #        from the user definition.  The format is X[-Y].
    # @return a dict with min/max fields; if max is not given,
    #         then min == max.  If the input is wrong, then just
    #         match every line.
    def __parse_line_interval(self, line_interval):
        interval_re = "^([0-9]+)(-([0-9]+))?$"
        match = re.match(interval_re, line_interval)
        if match:
            return dict(
                min=int(match.group(1)),
                max=int(match.group(3) if match.group(3) else match.group(1)),
            )

        # just match every line if bad interval was provided.
        return dict(min=0, max=float("inf"))


##
# Represent a loglevel.
#
# @param self the object itself.
# @param string the loglevel given as a string (DEBUG/ERROR/WARNING/...)
# @param level the loglevel given as for the 'logging' module API.
# @param function the native function from 'logging' module that
#        _actually_ outputs the log line.
class GnunetLoglevel:
    def __init__(self, string, level, function):
        self.string = string
        self.level = level
        self.function = function

    def __str__(self):
        return self.string

    def getLevel(self):
        return self.level

    def getFunction(self):
        return self.function


##
# The "mother" class of this module.  This class is in charge of
# parsing the definitions given by the user, from all the streams:
# being it programmatical, or the environment.  It is also in charge
# of giving the right precedence to the streams: e.g. GNUNET_FORCE_LOG
# takes precedence over the "setup()" method.
class GnunetLogger:

    COMPONENT_IDX = 0
    FILENAME_IDX = 1
    FUNCTION_IDX = 2
    LINE_INTERVAL = 3
    LEVEL_IDX = 4

    ##
    # Init contructor.
    #
    # @param self the object itself.
    # @param component the component name, that will be fed
    #        to the native 'logging' API.
    def __init__(self, component):
        self.logger = logging.getLogger(component)
        self.ERROR = GnunetLoglevel("ERROR", logging.ERROR, self.logger.error)
        self.WARNING = GnunetLoglevel("WARNING", logging.WARNING, self.logger.warning)
        self.INFO = GnunetLoglevel("INFO", logging.INFO, self.logger.info)
        self.DEBUG = GnunetLoglevel("DEBUG", logging.DEBUG, self.logger.debug)

        self.component = component
        self.loglevel = None

        # Setting the *logging* loglevel in order to have the
        # chance of changing the *logger* (object) loglevel along the
        # execution.  So this particular loglevel has no relevance
        # (might have been any other loglevel).
        logging.basicConfig(level=logging.INFO)

        self.no_forced_definitions = True
        self.definitions = list()

        # Give priority to the forced env.
        if os.environ.get("GNUNET_FORCE_LOG"):
            self.no_forced_definitions = False
            self.__parse_definitions(os.environ.get("GNUNET_FORCE_LOG"), True)

        if os.environ.get("GNUNET_LOG"):
            self.__parse_definitions(os.environ.get("GNUNET_LOG"), False)

        if os.environ.get("GNUNET_FORCE_LOGFILE"):
            filename = self.parse_filename(os.environ.get("GNUNET_FORCE_LOGFILE"))
            fh = logging.FileHandler(filename)
            self.logger.addHandler(fh)

    ##
    # Parse the filename where to write log lines.
    #
    # @param self the object itself.
    # @param filename the filename to parse (usually given
    #        to the '-l' option).
    # @return the parse filename string (with all the dates
    #         placeholders interpreted.)
    def parse_filename(self, filename):
        # implement {} and [] substitution.
        f = filename.replace("{}", self.component)
        f = f.replace("[]", str(os.getpid()))
        now = datetime.datetime.now()
        f = f.replace("%Y", now.strftime("%Y"))
        f = f.replace("%m", now.strftime("%m"))
        f = f.replace("%d", now.strftime("%d"))
        return f

    ##
    # Maps loglevels as strings, to loglevels as defined
    # in _this_ object.
    #
    # @param self the object itself.
    # @param level the string to map.
    # @return the loglevel native of _this_ object; defaults
    #         to INFO, if not found in the map.
    def string_to_loglevel(self, level):
        level_map = {
            "ERROR": self.ERROR,
            "WARNING": self.WARNING,
            "INFO": self.INFO,
            "DEBUG": self.DEBUG,
        }

        # Defaults to INFO.
        return level_map.get(level, self.INFO)

    ##
    # Set the loglevel for this module.
    def setup(self, loglevel):
        self.loglevel = loglevel

    ##
    # Log API for users to produce logs.
    #
    # @param self the object itself.
    # @param message the message to log.
    # @param message_loglevel the loglevel associated with the message.
    def log(self, message, message_loglevel):
        caller_frame = inspect.stack()[1]

        filename = os.path.basename(inspect.getfile(caller_frame[0]))
        lineno = caller_frame.lineno
        function = caller_frame.function

        # Ordinary case (level setup + nothing forced).
        if self.loglevel and self.no_forced_definitions:
            self.logger.setLevel(level=self.loglevel.getLevel())
            message_loglevel.getFunction()(message)
            return

        # We crawl through GNUNET_FORCE_LOG definitions,
        # or GNUNET_LOG (in case of non-forced definition
        # and non-given loglevel at object creation time)
        for defi in self.definitions:
            if defi.forced or not self.loglevel:
                if (
                    re.match(defi.component, self.component)
                    and re.match(defi.filename, filename)
                    and re.match(defi.function, function)
                    and defi.line_interval["min"] <= lineno <= defi.line_interval["max"]
                ):
                    self.logger.setLevel(
                        level=self.string_to_loglevel(defi.loglevel).getLevel()
                    )
                    message_loglevel.getFunction()(message)
                    return

        # If the flow got here, then one of the following
        # may hold.
        #
        # (1) GNUNET_FORCE_LOG was given and no definition was
        #     found for this component (neither forced nor unforced).
        #     Possibly, there also exists a default loglevel.

        if self.loglevel:
            self.logger.setLevel(level=self.loglevel.getLevel())

        # (2) GNUNET_FORCE_LOG was NOT given and neither was
        #     a default loglevel, and also a unforced definition
        #     wasn't found.  Must assign a made-up loglevel.

        else:
            self.logger.setLevel(level=logging.INFO)

        message_loglevel.getFunction()(message)

    ##
    # Helper function that parses definitions coming from the environment.
    #
    # @param self the object itself.
    # @param line the definition coming from the environment.
    # @param forced whether the definition comes from GNUNET_FORCE_LOG or not.
    def __parse_definitions(self, line, forced):
        gfl_split = line.split("/")
        for component in gfl_split:
            gfl_split_split = component.split(";")

            if 5 != len(gfl_split_split):
                print("warning: GNUNET_(FORCE_)LOG is malformed")
                return

            definition = LogDefinition(
                gfl_split_split[GnunetLogger.COMPONENT_IDX],
                gfl_split_split[GnunetLogger.FILENAME_IDX],
                gfl_split_split[GnunetLogger.FUNCTION_IDX],
                gfl_split_split[GnunetLogger.LINE_INTERVAL],
                gfl_split_split[GnunetLogger.LEVEL_IDX],
                forced,
            )

            self.definitions.append(definition)
