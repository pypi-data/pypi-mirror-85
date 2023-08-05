# This file is part of TALER
# (C) 2019 Taler Systems SA
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later
# version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA  02110-1301  USA
#
# @author Marcello Stanisci
# @version 0.0
# @repository https://git.taler.net/taler-util.git/

from unittest import TestCase
from taler.util.gnunet_log import GnunetLogger as GL
import os
from mock import patch, MagicMock
import logging
from datetime import datetime

# How the logging module defines loglevels.
#
# ERROR = 40
# WARNING = 30
# INFO = 20
# DEBUG = 10


##
# Helper function that removes any logging definition from the
# environment.
def clean_env():
    if os.environ.get("GNUNET_FORCE_LOG"):
        del os.environ["GNUNET_FORCE_LOG"]
    if os.environ.get("GNUNET_LOG"):
        del os.environ["GNUNET_LOG"]
    if os.environ.get("GNUNET_FORCE_LOGFILE"):
        del os.environ["GNUNET_FORCE_LOGFILE"]


##
# "mother" class of all the tests.  NOTE: no logs will appear
# on screen, as the setLevel function is mocked (therefore the
# level specified won't be made effective -- rather, only the
# default level (WARNING) will apply)!
class TestGnunetLog(TestCase):
    ##
    # Setup method; just take care of cleaning the environment.
    def setUp(self):
        clean_env()

    ##
    # This function tests whether GNUNET_FORCE_LOGFILE
    # is correctly interpreted.
    #
    # @param self the object itself.
    # @param mocked_FileHandler "mock" object that will
    #        "pretend" to be the file handler where the
    #        logging logic will register the logfile path.
    # @param mocked_addHandler "mock" object on which the
    #        logging logic is expected to register the @a
    #        mocked_FileHandler.
    @patch("logging.Logger.addHandler")
    @patch("logging.FileHandler")
    def test_force_logfile(self, mocked_FileHandler, mocked_addHandler):
        os.environ["GNUNET_FORCE_LOGFILE"] = "/tmp/{}-[]-%Y_%m_%d.log"
        unused_mock = MagicMock()
        mocked_FileHandler.return_value = unused_mock
        gl = GL("gnunet-pylog")
        gl.log("msg", gl.DEBUG)

        today = datetime.now()
        expected_filename = "/tmp/gnunet-pylog-%s-%s.log" % (
            str(os.getpid()),
            today.strftime("%Y_%m_%d"),
        )
        mocked_FileHandler.assert_called_with(expected_filename)
        mocked_addHandler.assert_called_with(unused_mock)

    ##
    # This function tests the very basic case, where no
    # env variable is set and no explicit loglevel is given
    # via the "setup()" method.  The expected result is that
    # the level is set to INFO.
    #
    # @param self the object itself.
    # @param mocked_basicConfig "mock" object that substitutes
    #        the real basicConfig.
    # @param mocked_setLevel "mock" object that substitutes
    #        the real setLevel.
    @patch("logging.Logger.setLevel")
    @patch("logging.basicConfig")
    def test_no_env_and_no_setup(self, mocked_basicConfig, mocked_setLevel):
        # Double-check no env variable gets in the way.
        self.assertIsNone(os.environ.get("GNUNET_FORCE_LOG"))
        self.assertIsNone(os.environ.get("GNUNET_LOG"))
        gl = GL("gnunet-pylog")
        gl.log("msg", gl.DEBUG)
        mocked_setLevel.assert_called_with(level=logging.INFO)

    ##
    # This function tests the case where *only* the GNUNET_LOG
    # env variable is set -- not even the manual setup of the
    # loglevel - via a call to the "setup()" method - is put in place.
    #
    # @param self the object itself.
    # @param mocked_basicConfig "mock" object that substitutes
    #        the real basicConfig.
    # @param mocked_setLevel "mock" object that substitutes
    #        the real setLevel.
    @patch("logging.Logger.setLevel")
    @patch("logging.basicConfig")
    def test_non_forced_env(self, mocked_basicConfig, mocked_setLevel):
        self.assertIsNone(os.environ.get("GNUNET_FORCE_LOG"))
        os.environ[
            "GNUNET_LOG"
        ] = "gnunet-pylog;log_test.py;test_non_forced_env;99;ERROR"  # lineno is not 100% accurate.
        gl = GL("gnunet-pylog")
        gl.log("msg", gl.DEBUG)
        mocked_setLevel.assert_called_with(level=logging.INFO)

    ##
    # This function tests the case where *only* the GNUNET_FORCE_LOG
    # env variable is set -- not even the manual setup of the loglevel
    # is put in place.
    #
    # @param self the object itself.
    # @param mocked_basicConfig "mock" object that substitutes
    #        the real basicConfig.
    # @param mocked_setLevel "mock" object that substitutes
    #        the real setLevel.
    @patch("logging.Logger.setLevel")
    @patch("logging.basicConfig")
    def test_only_forced_env(self, mocked_basicConfig, mocked_setLevel):
        self.assertIsNone(os.environ.get("GNUNET_LOG"))
        os.environ[
            "GNUNET_FORCE_LOG"
        ] = "gnunet-pylog;log_test.py;test_only_forced_env;90-200;ERROR"
        gl = GL("gnunet-pylog")
        gl.log("msg", gl.DEBUG)
        mocked_setLevel.assert_called_with(level=logging.INFO)

    ##
    # This function tests the case where *only* the manual
    # loglevel setup is put in place.
    #
    # @param self the object itself.
    # @param mocked_basicConfig "mock" object that substitutes
    #        the real basicConfig.
    # @param mocked_setLevel "mock" object that substitutes
    #        the real setLevel.
    @patch("logging.Logger.setLevel")
    @patch("logging.basicConfig")
    def test_only_manual_loglevel_setup(self, mocked_basicConfig, mocked_setLevel):
        self.assertIsNone(os.environ.get("GNUNET_LOG"))
        self.assertIsNone(os.environ.get("GNUNET_FORCE_LOG"))
        gl = GL("gnunet-pylog")
        gl.setup(gl.ERROR)
        gl.log("msg", gl.DEBUG)
        mocked_setLevel.assert_called_with(level=logging.ERROR)

    ##
    # This function tests the case where *both* the manual loglevel
    # and the forced env variable are setup; the expected result is
    # that the forced variable wins over the manual setup.
    #
    # @param self the object itself.
    # @param mocked_basicConfig "mock" object that substitutes
    #        the real basicConfig.
    # @param mocked_setLevel "mock" object that substitutes
    #        the real setLevel.
    @patch("logging.Logger.setLevel")
    @patch("logging.basicConfig")
    def test_manual_loglevel_AND_forced_env(self, mocked_basicConfig, mocked_setLevel):
        self.assertIsNone(os.environ.get("GNUNET_LOG"))
        self.assertIsNone(os.environ.get("GNUNET_FORCE_LOG"))

        # forced env definition (*before* object creation)
        os.environ["GNUNET_FORCE_LOG"] = ";;;;ERROR"
        gl = GL("gnunet-pylog")

        # manual setup
        gl.setup(gl.WARNING)

        gl.log("msg", gl.DEBUG)
        mocked_setLevel.assert_called_with(level=logging.ERROR)

    ##
    # This function tests the case where *both* GNUNET_LOG and
    # the manual loglevel setup are put in place.  The expectation
    # is that the manual loglevel wins.
    #
    # @param self the object itself.
    # @param mocked_basicConfig "mock" object that substitutes
    #        the real basicConfig.
    # @param mocked_setLevel "mock" object that substitutes
    #        the real setLevel.
    @patch("logging.Logger.setLevel")
    @patch("logging.basicConfig")
    def test_manual_loglevel_AND_nonforced_env(
        self, mocked_basicConfig, mocked_setLevel
    ):
        self.assertIsNone(os.environ.get("GNUNET_LOG"))
        self.assertIsNone(os.environ.get("GNUNET_FORCE_LOG"))
        os.environ["GNUNET_LOG"] = ";;;;DEBUG"
        gl = GL("gnunet-pylog")
        gl.setup(gl.ERROR)
        gl.log("msg", gl.DEBUG)
        mocked_setLevel.assert_called_with(level=logging.ERROR)

    ##
    # This function tests the case where *both* GNUNET_LOG and
    # GNUNET_FORCE_LOG are defined.  The expectation is that the
    # forced variable wins.
    #
    # @param self the object itself.
    # @param mocked_basicConfig "mock" object that substitutes
    #        the real basicConfig.
    # @param mocked_setLevel "mock" object that substitutes
    #        the real setLevel.
    @patch("logging.Logger.setLevel")
    @patch("logging.basicConfig")
    def test_forced_env_AND_nonforced_env(self, mocked_basicConfig, mocked_setLevel):
        self.assertIsNone(os.environ.get("GNUNET_LOG"))
        self.assertIsNone(os.environ.get("GNUNET_FORCE_LOG"))
        os.environ["GNUNET_LOG"] = ";;;;DEBUG"
        os.environ["GNUNET_FORCE_LOG"] = ";;;;ERROR"
        gl = GL("gnunet-pylog")
        gl.log("msg", gl.DEBUG)
        mocked_setLevel.assert_called_with(level=logging.ERROR)
