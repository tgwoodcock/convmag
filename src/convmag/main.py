"""
This module contains the code for the interactive conversion
of units at the command line.

@author: tgwoodcock
"""

from .__init__ import __version__
from . import convmag_functions as cm


# interactive conversion
def main():
    CONVERTING = True
    print(f"convmag {__version__}\n")
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
            print("\n".join(cm.units)+"\nmuB/fu")
            print("\nThe prefactors available for any base unit are:",
                  ", ".join(cm.prefactors))
        elif r == "conv":
            lgst = max(map(len, cm.units))
            print("\nThe conversions between base units available are:")
            for k in list(cm.convmag.keys()):
                St, En = k.split("_")
                print(f"{St:>{lgst}}  <->  {En:<{lgst}}:    {cm.convmag[k]}")
            print(f"{'muB/fu':>{lgst}}  <->  {'T':<{lgst}}:    requires user input")
            print("\nINFO: the factors given above are for the forward conversion")
            print("INFO: permeability of free space, MU_0 = 4 * 3.14159 * 1e-7 H/m (== Vs/Am)")
            print("INFO: Bohr magneton, MU_B =  9.274015e-24 Am^2")
            print("      (muB is the unit string for conversions with Bohr magnetons)")
            print("INFO: prefactors available for any base unit:",
                  ", ".join(cm.prefactors))

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
                    vol = cm.calculate_unitcell_volume(a, b, c, gamma=120)
                elif gamma == "90":
                    vol = cm.calculate_unitcell_volume(a, b, c)
                vol = vol * (1E-10)**3 # to get m^3 from A^3
                print("Please enter the number of formula units per unit cell:")
                num_fu = int(input("f.u./unit cell: "))
                if startunit == "muB/fu":
                    Tesla = cm.muB_per_fu_to_Tesla(val, num_fu, vol)
                    s1 = f"\n{val} muB per f.u. = {Tesla:.5f} T"
                    s2 = f" ({num_fu:d} f.u./unit cell, "
                    s3 = f"cell volume = {vol:.3e} m^3)"
                    print("".join([s1, s2, s3]))

                elif startunit == "T":
                    muB_fu = cm.Tesla_to_muB_per_fu(val, num_fu, vol)
                    s1 = f"\n{val} T = {muB_fu:.5f} muB per f.u."
                    s2 = f" ({num_fu:d} f.u./unit cell, "
                    s3 = f"cell volume = {vol:.3e} m^3)"
                    print("".join([s1, s2, s3]))

            else:
                cm.convert_unit(val, startunit, endunit, verbose=True)
