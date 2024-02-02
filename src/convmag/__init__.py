"""
Conversions between various magnetic units.

There are two ways to use this program:

1) as a simple command line tool for converting units. In this
   case only single values can be converted (at one time)

2) import this paakage into python and then you can pass numpy arrays
   into convert_unit(), making sure to keep the default verbose=False.
   That way many values can be converted at once. The converted
   values are returned as a numpy array for further processing.

@author: tgwoodcock

Pure python version, no imports needed.

Requires Python >= 3.6 because f-strings are used
"""

__version__ = '0.0.4'

from .convmag_functions import *
