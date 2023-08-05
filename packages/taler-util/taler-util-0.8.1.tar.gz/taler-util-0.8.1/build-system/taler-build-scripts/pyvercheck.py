# This file is placed in the public domain.

import sys

if sys.version_info.major < 3 or sys.version_info.minor < 7:
    sys.stderr.write("error: python>=3.7 must be available as the python3 executable\n")
    sys.exit(1)
