# The MIT License (MIT)
#
# Copyright (c) 2020 Kattni Rembor for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
Verifies which board is being used and imports the appropriate module.
"""

import os

if "CLUE" in os.uname().machine:
    from .clue import clue as pybadger
elif "Pybadge" in os.uname().machine:
    from .pybadge import pybadge as pybadger
elif "PyGamer" in os.uname().machine:
    from .pygamer import pygamer as pybadger
elif "PewPew M4" in os.uname().machine:
    from .pewpewm4 import pewpewm4 as pybadger
elif "PyPortal" in os.uname().machine:
    from .pyportal import pyportal as pybadger
elif "Circuit Playground Bluefruit" in os.uname().machine:
    from .cpb_gizmo import cpb_gizmo as pybadger
elif "MagTag with ESP32S2" in os.uname().machine:
    from .mag_tag import mag_tag as pybadger
