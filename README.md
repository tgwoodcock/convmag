[![PyPI Version](https://img.shields.io/pypi/v/convmag.svg)](https://pypi.python.org/pypi/convmag/)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/convmag.svg)](https://pypi.python.org/pypi/convmag/)

# convmag
Conversion between various units used in magnetism

The conversions between *base units* available are:
        
             T  <->  G         :    1e4
             T  <->  Oe        :    1e4
           A/m  <->  T         :    MU_0
           A/m  <->  G         :    1e4 * MU_0
             G  <->  Oe        :    1
           A/m  <->  Oe        :    1e4 * MU_0
      emu/cm^3  <->  T         :    1e3 * MU_0
    erg/Oecm^3  <->  A/m       :    1e3
         emu/g  <->  Am^2/kg   :    1
         J/m^3  <->  GOe       :    1e8 * MU_0
         J/m^3  <->  erg/cm^3  :    1e1
      erg/cm^3  <->  GOe       :    1e7 * MU_0
          Am^2  <->  emu       :    1e3
          Am^2  <->  erg/G     :    1e3
          Am^2  <->  erg/Oe    :    1e3
           emu  <->  erg/G     :    1
           muB  <->  Am^2      :    MU_B
           muB  <->  emu       :    1e3 * MU_B
        muB/fu  <->  T         :    requires user input of lattice parameters

(the factors given above are for the forward conversion)

- permeability of free space, MU_0 = 4 * 3.14159 * 1e-7 H/m  (== Vs/Am)

- Bohr magneton, MU_B =  9.274015e-24 Am^2
      (muB is the unit string for conversions with Bohr magnetons)

The *prefactors* available for any base unit are: M (1e6), k (1e3), m (1e-3), µ (1e-6)

You can combine *prefactors* and *base units* to give e.g. MA/m or kJ/m^3

<br>

### A word about emu

emu is not a unit but indicates the system of cgs units being used (emu == electromagnetic units)

The magnetisation data from magnetometers is very often given in emu, and in these cases emu implies the units erg/G. 
This is why the equivalence emu = erg/G is given above. Many authors still quote emu/g or emu/cm^3 and therefore,
these conversions are listed in the table above. convmag always assumes that emu has the units erg/G.

**In some cases emu may take other units, so it's always worth checking this!** 

<br>

## Installation:

### Pip
You can install the current release (0.0.3) with pip:
```bash
    pip install convmag
```

Pure python, no other dependencies.

Requires Python >= 3.6 because f-strings are used

<br>

## Usage options:

1) a console script is provided and should be located in the Scripts directory of
   your Python distribution after installation. If you have this directory in
   your Path (environment variable on Windows) you can start the program by
   typing "convmag" in the console. In this case only single values can be 
   converted (at one time).

2) the package can be imported into python and then you can pass numpy arrays
   into the function convert_unit(), making sure to keep the default verbose=False.
   That way many values can be converted at once. The converted
   values are returned as a numpy array for further processing.
   
```python
    >>> import numpy as np
    >>> import convmag as cm
    
    >>> vals_in_T = np.arange(0,130,20)
    
    >>> vals_in_T
    array([  0,  20,  40,  60,  80, 100, 120])
   
    >>> vals_in_Oe = cm.convert_unit(vals_in_T, "T", "Oe", verbose=False)
    
    >>> vals_in_Oe
    array([      0.,  200000.,  400000.,  600000.,  800000., 1000000., 1200000.])
```

<br>

## Converting between Bohr Magnetons per formula unit and Tesla (muB/fu <-> T)

This conversion requires user input of:

- the lattice parameters *a*, *b*, *c* and *gamma*, and

- the number of formula units per unit cell.

Only orthogonal (cubic, tetragonal and orthorhombic) and hexagonal unit cells can be handled
and therefore *gamma* = 90° or 120°.

As an example of the number of formula units per unit cell, Nd2Fe14B is the formula unit, which
has 17 atoms, and the unit cell contains 68 atoms, so in this case there are 4 formula units per unit cell.

Calling convmag in the console, the conversion from muB to T looks like this:

```
    Input: 2.3 muB/fu T

    ***INFO: muB per formula unit <-> T***

    Please enter lattice parameters: a b c in Angstrom
    a b c: 3.0 3.0 4.0

    Limited to orthogonal or hexagonal unit cells:
    Please enter gamma in deg. (90 or 120): 90
    Please enter the number of formula units per unit cell:
    f.u./unit cell: 2

    2.3 muB per f.u. = 1.48913 T (2 f.u./unit cell, cell volume = 3.600e-29 m^3)
```

