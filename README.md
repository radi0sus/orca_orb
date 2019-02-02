orca_orb.py 
===========

Analyzes the section 'LOEWDIN REDUCED ORBITAL POPULATIONS PER MO' in ORCA output files.

ORCA: https://orcaforum.kofo.mpg.de/

Output will be written to 'o-analysis.txt'. Up to four plots will be created.
The program needs write permissions in the output folder!

Usage:
    
    (python) orca_orb.py -options ORCA.out

Options are `-t, -o, -c, -ncsv` (see below).


Naming conventions
------------------
* Atoms are numbered items, e.g. 0, 1, 2, 3 (which are associated to Elements)
* Elements are elements of the periodic table, e.g. C, N
* Orbital refers to the orbital in the 'LOEWDIN REDUCED ORBITAL POPULATIONS PER MO' section
* Atomic orbitals or AOs are s, p, d, and f orbitals
* Contributions to orbitals (in %) can be contributions from Atoms, a group of Atoms (=Elements) 
  and/or AOs. 
* The sum of all contributions of Atoms of the same Element is equal to the contribution of the respective 
  Element to the orbital.
* If a contribution or a sum of contributions is lower than a certain Trehshold the contribution may
  not be included in the output of the program.
* Constraints refer to a selection of analyzed Atom or Element contributions.


Output
------
`O-analysis.txt` contains tables that summarize contributions of elements (C, N, O, Fe...), 
atoms (0, 1, 2 as they appear in the input) and AOs (s, p, d, f) to orbitals listed under 
'LOEWDIN REDUCED ORBITAL POPULATIONS PER MO'. In case of spin unrestricted calculations 
contributions to alpha and beta orbitals are listed separately. All contributions are given in '%'.


Threshold (-t, --threshold)
---------------------------
To reduce the size of the output a threshold in '%' can be defined (-t or --threshold). Only
(summarized) atom (including AOs) contributions higher or equal to the given threshold will
be printed. The threshold is not valid for the first (two) tables (element contributions to orbitals)
and the bar plot(s).


Bar plot(s)
-----------
The bar plot `el-cntrb-a.png` visualizes the contribution (in %) of elements to orbitals. A given
threshold or constraints are not valid for this plot. In case of spin unrestricted calculations 
respective plots for alpha (...-a.png) and beta (...-b.png) orbitals will be created.


Heat map(s)
-----------
The heat map `a-cntrb-a.png` shows the contribution (in %) of atoms to orbitals. Values are printed
if the size of the heat map is not to large. Otherwise different colors indicate high or low 
contributions. All contribution below the threshold or zero contributions are '0' or have a black color.
In case of spin unrestricted calculations respective plots for alpha (...-a.png) and beta (...-b.png) 
orbitals will be created.


Orbital range (-o, --orbitals)
------------------------------
A range of orbitals can be defined with the '-o' (--orbitals) parameter. It should be noted that all
orbitals from the ORCA output will be processed first and that the orbital selection is done in a
second step. 
At least one argument is expected after '-o'. If the '-o' parameter is not given all orbitals will 
be included in the analysis.

Examples:
    
    -o3            : processes orbital number 3
    -oh or oHOMO   : processes the HOMO
    -oh10          : processes all orbitals from HOMO-10 to HOMO+10
    -o0-10 or o0:10: processes all orbitals from 0 to 10


Atom or element constriants (-c, --constriants)
-----------------------------------------------
Analysis can be constrained to selected elements or atoms using the '-c' (--constraints) parameter. Elements 
or atoms not present in the ORCA output file will be ignored without warning. The input is case sensitive and  
multiple elements or atoms have to be separated by commas (','). Atom and elements constraints cannot be mixed.
At least one argument is expected after '-c'.If the '-c' parameter is not given, all atoms and elements
will be included in the analysis. The constraints are not valid for the first (two) tables (element contributions 
to orbitals) and the bar plot(s).

Examples:
    
    -cC      : analysis is constrained to carbon atoms
    -cC,N    : analysis is constrained to carbon and nitrogen atoms
    -cC,N,Zz : analysis is constrained to carbon and nitrogen atoms, 
               since element 'Zz' has not been found in the ORCA output file 
    -c1      : analysis is constrained to atom 1
    -c1,4,5  : analysis is constrained to atom 1, 4 & 5
    
    -c1,N    : not possible: analysis is constrained to atom 1, N will be ignored
    -cC,3    : not possible: analysis is constrained to carbon atoms, 3 will be ignored
    -c1N     : not possible: analysis is constrained to atom 1, N will be ignored
    -cC3     : not possible: analysis is constrained to carbon atoms, 3 will be ignored


CSV file and -ncsv (--newcsv) option
------------------------------------
In a first step all information listed under 'LOEWDIN REDUCED ORBITAL POPULATIONS PER MO' will be read,
and written to a large table. The naming scheme is 'orca.out.csv'. In subsequent analyses the program
uses this file which makes analyses much faster. For creating a new CSV file, the option '-ncsv' can be used.


Example inputs
--------------
Threshold and constraints are not valid for the first (two) tables (element contributions to orbitals)
and the bar plot(s).

Orbitals from HOMO-10 to HOMO+10 with iron contributions >= 5% will be analyzed: 

    orca_orb.py -t5 -cFe -oh10 my-calc.out
    
Orbitals from 0 to 10 with contributions of atoms 1 & 3 >= 10% will be analyzed:
    
    orca_orb.py -t10 -c1,3 -o0:10 my-calc.out
    
All orbitals with contributions from all elements (or all atoms) >= 4.2% will be analyzed:
    
    orca_orb.py -t4.2 my-fe-calc.out
    
 
Have fun!


#### Check https://github.com/radi0sus for updates.
