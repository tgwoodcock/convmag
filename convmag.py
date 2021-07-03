"""
Conversions between various magnetic units.

There are two ways to use this program:

1) as a simple command line tool for converting units. In this
   case only single values can be converted (at one time)

2) import this module into python and then you can pass numpy arrays
   into convert_unit(), making sure to keep the default verbose=False.
   That way many values can be converted at once. The converted
   values are returned as a numpy array for further processing.

@author: tgwoodcock

This version: July 2021

Pure python version, no imports needed.

Requires Python >= 3.6 because f-strings are used
"""

MU_0 = 4 * 3.14159 * 1e-7 # permeability of free space in Vs/Am
MU_B = 9.274015e-24 # Bohr magneton in Am^2

convmag = {"T_G" : "1e4",
           "T_Oe" : "1e4",
           "A/m_T" : "MU_0",
           "A/m_G" : "1e4 * MU_0",
           "G_Oe" : "1",
           "A/m_Oe" : "1e3 * MU_0",
           "emu/cm^3_T" : "1e3 * MU_0",
           "erg/Oecm^3_A/m" : "1e3",

           "emu/g_Am^2/kg" : "1",

           "J/m^3_GOe" : "1e8 * MU_0",
           "J/m^3_erg/cm^3" : "1e1",
           "GOe_erg/cm^3" : "1e3 * MU_0",

           "Am^2_emu" : "1e3",
           "Am^2_erg/G" : "1e3",
           "Am^2_erg/Oe" : "1e3",
           "emu_erg/G" : "1",
           "muB_Am^2" : "MU_B",
           "muB_emu" : "1e3 * MU_B"
           }

factors = {"M" : "1e6",
           "k" : "1e3",
           "m" : "1e-3",
           "µ" : "1e-6"
           }


units = {i for a in [x.split("_") for x in list(convmag.keys())] for i in a}
prefactors = [f"{k} ({factors[k]})" for k in factors]


def convert_unit(number, startunit, endunit, verbose=False):
    """
    Convert number startunits to endunits.
    The dict "convmag" holds the conversion factors.


    Parameters
    ----------
    number : FLOAT or NDARRAY
        a float or nd-array containing the value(s) to be converted.
    startunit : STR
        str containing the initial unit.
    endunit : STR
        str containing the target unit.
    verbose : BOOLEAN, optional
        If True, the converted value will be printed as well as
        returned. This does not work if an array of values is
        passed for conversion therefore: The default is False.

    Returns
    -------
    conv : FLOAT or NDARRAY
        the number(s) converted from startunits to endunits.

    """
    if startunit in units:
        s_u = startunit
        pre = "1"
    elif startunit[0] in list(factors) and startunit[1:] in units:
        s_u = startunit[1:]
        pre = factors[startunit[0]]
    else:
        print("\n*****Unit Error in convert_unit()*****")
        print("Start unit not recognised!")
        s_u = ""
        pre = "1"

    if endunit in units:
        e_u = endunit
        post = "1"
    elif endunit[0] in list(factors) and endunit[1:] in units:
        e_u = endunit[1:]
        post = factors[endunit[0]]
    else:
        print("\n*****Unit Error in convert_unit()*****")
        print("End unit not recognised!")
        e_u = ""
        post = "1"

    conv = None
    key = s_u+'_'+e_u
    try:
        conv = number * eval(pre) *eval(convmag[key]) / eval(post)
    except KeyError:
        try:
            key_alt = e_u+'_'+s_u
            conv = number * eval(pre) * (1./eval(convmag[key_alt])) / eval(post)
        except KeyError:
            if s_u in units and e_u in units:
                print("\n*****Unit Error in convert_unit()*****")
                print(f"Conversion not available: {startunit} to {endunit}")

    if verbose and conv is not None:
        if 1e3 >= conv >= 1e-3:
            print(f"{number} {startunit} = {conv:.5f} {endunit}")
        else:
            print(f"{number} {startunit} = {conv:.5e} {endunit}")

    return conv


def calculate_unitcell_volume(a, b, c, gamma=90):
    """
    Calculates the volume of a unit cell.

    a,b,c = lattice paramters in Angstrom

    gamma = lattice parameter in degrees.

    INFO: handles only orthogonal and hexagonal cases!

    Parameters
    ----------
    a : FLOAT
        Lattice parameter, a
    b : FLOAT
        Lattice parameter, b
    c : FLOAT
        Lattice parameter, c
    gamma : INT or FLOAT, optional
        Lattice parameter, gamma in degrees. The default is 90.

    Returns
    -------
    vol : FLOAT
        The unit cell volume calculated from the input lattice
        parameters. The unit is the cube of the unit used for a, b and c.

    """
    if gamma == 90:
        vol = a*b*c
    elif gamma == 120:
        vol = 0.866*a**2*c # hexagonal case

    return vol


def muB_per_fu_to_Tesla(muB_per_fu, num_fu, vol):
    """
    Calculate the polarisation in Tesla given
    the moment in Bohr magnetons per formula unit, the number of formula
    units per unit cell and the volume of the unit cell (in m^3).

    1 muB = 9.274015E-24 Am^2.
    Source: Coey, Magnetism and Magnetic Materials, p617 (list of constants)


    Parameters
    ----------
    muB_per_fu : INT or FLOAT
        Moment in Bohr magnetons per formula unit (a.k.a. muB/f.u.)
    num_fu : INT
        number of formula units per unit cell
    vol : FLOAT
        volume of the unit cell in m^3.

    Returns
    -------
    polarisation : FLOAT
        the magnetic polarisation in Tesla

    """
    moment = muB_per_fu * num_fu * MU_B
    moment_vol = moment / vol
    polarisation = moment_vol * MU_0
    return polarisation


def Tesla_to_muB_per_fu(polarisation, num_fu, vol):
    """
    Calculate the magnetisation in Bohr magnetons per formula unit
    from the polarisation in Tesla, the unit cell volume in m^3 and
    the number of formula units per unit cell.

    1 muB = 9.274015E-24 Am^2.
    Source: Coey, Magnetism and Magnetic Materials, p617 (list of constants)

    Tesla: the magnetisation in Tesla
    num_fu = number of formula units per unit cell
    vol = volume of the unit cell in cm^3.

    Parameters
    ----------
    polarisation : FLOAT
        the magnetic polarisation in Tesla
    num_fu : INT
        number of formula units per unit cell
    vol : FLOAT
        volume of the unit cell in m^3.

    Returns
    -------
    muB_per_fu : FLOAT
        Moment in Bohr magnetons per formula unit (a.k.a. muB/f.u.)

    """
    moment_vol = polarisation / MU_0
    moment = moment_vol * vol
    muB_per_fu = moment / (num_fu * MU_B)
    return muB_per_fu


# interactive conversion
if __name__ == '__main__':
    CONVERTING = True
    print("*****Conversion between magnetic units.*****")
    print("\nAt the 'Input:' promt, enter:")
    print("[value startunit endunit] e.g. 6 T A/m,")
    print("[units] to list the available units,")
    print("[conv] to list the conversion factors or")
    print("[q] to quit.")
    while CONVERTING:
        r = input("\nInput: ")
        if r == "q":
            CONVERTING = False
        elif r == "units":
            print("\nThe base units available for conversion are:")
            print("\n".join(units)+"\nmuB/fu")
            print("\nThe prefactors available for any base unit are:",
                  ", ".join(prefactors))
        elif r == "conv":
            lgst = max(map(len, units))
            print("\nThe conversions between base units available are:")
            for k in list(convmag.keys()):
                St, En = k.split("_")
                print(f"{St:>{lgst}}  <->  {En:<{lgst}}:    {convmag[k]}")
            print(f"{'muB/fu':>{lgst}}  <->  {'T':<{lgst}}:    requires user input")
            print("\nINFO: the factors given above are for the forward conversion")
            print("INFO: permeability of free space, MU_0 = 4 * 3.14159 * 1e-7 Vs/Am")
            print("INFO: Bohr magneton, MU_B =  9.274015e-24 Am^2")
            print("      (muB is the unit string for conversions with Bohr magnetons)")
            print("INFO: prefactors available for any base unit:",
                  ", ".join(prefactors))

        else:
            val = float(r.split(" ")[0])
            startunit = r.split(" ")[1]
            endunit = r.split(" ")[2]
            if "muB/fu" in [startunit, endunit] and "T" in [startunit, endunit]:
                print("\n***INFO: muB per formula unit <-> T***\n")
                print("Please enter lattice parameters: a b c in Angstrom")
                lp = input("a b c: ")
                a = float(lp.split(" ")[0])
                b = float(lp.split(" ")[1])
                c = float(lp.split(" ")[2])
                print("\nLimited to orthogonal or hexagonal unit cells:")
                gamma = input("Please enter gamma in deg. (90 or 120): ")
                if gamma == "120":
                    vol = calculate_unitcell_volume(a, b, c, gamma=120)
                elif gamma == "90":
                    vol = calculate_unitcell_volume(a, b, c)
                vol = vol * (1E-10)**3 # to get m^3 from A^3
                print("Please enter the number of formula units per unit cell:")
                num_fu = int(input("f.u./unit cell: "))
                if startunit == "muB/fu":
                    Tesla = muB_per_fu_to_Tesla(val, num_fu, vol)
                    s1 = f"\n{val} muB per f.u. = {Tesla:.5f} T"
                    s2 = f" ({num_fu:d} f.u./unit cell, "
                    s3 = f"cell volume = {vol:.3e} m^3)"
                    print("".join([s1, s2, s3]))

                elif startunit == "T":
                    muB_fu = Tesla_to_muB_per_fu(val, num_fu, vol)
                    s1 = f"\n{val} T = {muB_fu:.5f} muB per f.u."
                    s2 = f" ({num_fu:d} f.u./unit cell, "
                    s3 = f"cell volume = {vol:.3e} m^3)"
                    print("".join([s1, s2, s3]))

            else:
                convert_unit(val, startunit, endunit, verbose=True)
