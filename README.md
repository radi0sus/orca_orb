# orca_orb

Analyzes the section 'LOEWDIN REDUCED ORBITAL POPULATIONS PER MO' in ORCA output files.

ORCA: https://orcaforum.kofo.mpg.de/

Output will be written to 'o-analysis.txt'. Up to four plots will be created.
The program needs write permissions in the output folder!

Usage:
(python) orca_orb.py -options ORCA.out

Options are -t, -o, -ncsv (see below).

'O-analysis.txt' contains tables that summarize contributions of elements (C, N, O, Fe...), 
atoms (0, 1, 2 as they appear in the input) and AOs (s, p, d, f) to orbitals listed under 
'LOEWDIN REDUCED ORBITAL POPULATIONS PER MO'. In case of spin unrestricted calculations 
contributions to alpha and beta orbitals are listed separately. All contributions are given in '%'.

To reduce the size of the output a threshold in '%' can be defined (-t or --threshold). Only
(summarized) atom (including AOs) contributions higher or equal to the given threshold will
be printed. The threshold is not valid for element contributions to orbitals.

The bar plot 'el-cntrb-a.png' visualizes the contribution (in %) of elements to orbitals. A given
threshold is not valid for this plot.

The heat map 'a-cntrb-a.png' shows the contribution (in %) of atoms to orbitals. Values are printed
if the size of the heat map is not to large. Otherwise different colors indicate high or low 
contributions. All contribution below the threshold ore zero contributions are '0' or have a black color.
In case of spin unrestricted calculations respective plots for alpha (...-a.png) and beta (...-b.png) 
orbitals will be created.

A range of orbitals can be defined with the '-o' (--orbitals) parameter. It should be noted that all
orbitals from the ORCA output will be processed first and that the orbital selection is done in a
second step.
-If the -o parameter is not given or empty all orbitals will be analyzed and printed. 
-o3            : processes orbital number 3
-oh or oHOMO   : processes the HOMO
-oh10          : processes all orbitals from HOMO-10 to HOMO+10
-o0-10 or o0:10: processes all orbitals from 0 to 10

In a first step all information listed under 'LOEWDIN REDUCED ORBITAL POPULATIONS PER MO' will be read,
and written to a large table. The naming scheme is 'orca.out.csv'. In subsequent analyses the program
uses this file which makes analyses much faster. For creating a new CSV file, the option '-ncsv' can be used.

Have fun!
