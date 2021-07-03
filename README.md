# convmag
Conversion between various units used in magnetism

The conversions between *base units* available are:
        
             T  <->  G         :    1e4
             T  <->  Oe        :    1e4
           A/m  <->  T         :    MU_0
           A/m  <->  G         :    1e4 * MU_0
             G  <->  Oe        :    1
           A/m  <->  Oe        :    1e3 * MU_0
      emu/cm^3  <->  T         :    1e3 * MU_0
    erg/Oecm^3  <->  A/m       :    1e3
         emu/g  <->  Am^2/kg   :    1
         J/m^3  <->  GOe       :    1e8 * MU_0
         J/m^3  <->  erg/cm^3  :    1e1
           GOe  <->  erg/cm^3  :    1e3 * MU_0
          Am^2  <->  emu       :    1e3
          Am^2  <->  erg/G     :    1e3
          Am^2  <->  erg/Oe    :    1e3
           emu  <->  erg/G     :    1
           muB  <->  Am^2      :    MU_B
           muB  <->  emu       :    1e3 * MU_B
        muB/fu  <->  T         :    requires user input of lattice parameters

(the factors given above are for the forward conversion)

- permeability of free space, MU_0 = 4 * 3.14159 * 1e-7 Vs/Am

- Bohr magneton, MU_B =  9.274015e-24 Am^2
      (muB is the unit string for conversions with Bohr magnetons)

The *prefactors* available for any base unit are: M (1e6), k (1e3), m (1e-3), µ (1e-6)

<br>

### Ways to use this program:
1) as a simple command line tool for converting units. In this
   case only single values can be converted (at one time)

2) import this module into python and then you can pass numpy arrays
   into convert_unit(), making sure to keep the default verbose=False.
   That way many values can be converted at once. The converted
   values are returned as a numpy array for further processing.

Pure python, no imports needed.

Requires Python >= 3.6 because f-strings are used
