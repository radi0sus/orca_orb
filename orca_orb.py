# -*- coding: utf-8 -*-
'''
orca_orb.py 
===========

Analyzes the section 'LOEWDIN REDUCED ORBITAL POPULATIONS PER MO' in ORCA output files.

ORCA: https://orcaforum.kofo.mpg.de/

Output will be written to 'o-analysis.txt'. Up to four plots will be created.
The program needs write permissions in the output folder!

Usage:
    
    (python) orca_orb.py -options ORCA.out

Options are `-t`, `-o`, `-c`, `-a`, -`ncsv` (see below).


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
* If a contribution or a sum of contributions is lower than a certain Threshold the contribution may
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
To reduce the size of the output a threshold in '%' can be defined (`-t` or `--threshold`). Only
(summarized) atom (including AOs) contributions higher or equal to the given threshold will
be printed. The threshold is not valid for the first (two) tables (element contributions to orbitals)
and the bar plot(s).


Bar plot(s)
-----------
The bar plot `el-cntrb-a.png` visualizes the contribution (in %) of elements to orbitals. A given
threshold or constraints are not valid for this plot. In case of spin unrestricted calculations 
respective plots for alpha (...-a.png) and beta (...-b.png) orbitals will be created.

Restarting the program deletes all plots.


Heat map(s)
-----------
The heat map `a-cntrb-a.png` shows the contribution (in %) of atoms to orbitals. Values are printed
if the size of the heat map is not to large. Otherwise different colors indicate high or low 
contributions. All contribution below the threshold or zero contributions are '0' or have a black color.
In case of spin unrestricted calculations respective plots for alpha (...-a.png) and beta (...-b.png) 
orbitals will be created.

The heat map `ao-cntrb-Element/Atom-a.png` shows the contribution (in %) of the atomic orbitals (s, p, d, f) 
of a specific atom in a range of orbitals. The heat map will be created if the `-a` parameter is invoked with 
a specific atom number or atom numbers, e.g. `-a0` or `-a0,1,2`.
All contribution below the threshold or zero contributions are '0' or have a black color. A heat map
for a selected atom might not be created if the contribution of the atom (or the respective AOs) is 
below a given threshold in the selected orbital range.
In case of spin unrestricted calculations respective plots for alpha (...-a.png) and beta (...-b.png) 
orbitals will be created. 

Restarting the program deletes all plots.


Orbital range (-o, --orbitals)
------------------------------
A range of orbitals can be defined with the `-o (--orbitals)` parameter. It should be noted that all
orbitals from the ORCA output will be processed first and that the orbital selection is done in a
second step. 
At least one argument is expected after `-o`. If the `-o` parameter is not given all orbitals will 
be included in the analysis.

Examples:
    
    -o3            : processes orbital number 3
    -oh or oHOMO   : processes the HOMO
    -oh10          : processes all orbitals from HOMO-10 to HOMO+10
    -o0-10 or o0:10: processes all orbitals from 0 to 10


Atom or element constraints (-c, --constraints)
-----------------------------------------------
Analysis can be constrained to selected elements or atoms using the `-c (--constraints)` parameter. Elements 
or atoms not present in the ORCA output file will be ignored without warning. The input is case sensitive and  
multiple elements or atoms must be separated by commas (','). Atom and elements constraints cannot be mixed.
At least one argument is expected after `-c`. If the `-c` parameter is not given, all atoms and elements
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

    
AOs in orbital plots (-a, --aorbitals)
--------------------------------------
The `-a` parameter with atom (numbers) as additional argument(s) creates the AOs in orbitals heat maps. 
If constraints are operative they might interfere with atoms given after `-a`. So if carbon atoms are excluded
from the analysis, a heat map of the AOs of carbon atom 5 (`-a5`) will not be created. Threshold is effective 
as well. See the 'Heat map(s)' section for more details.
In case of spin unrestricted calculations respective plots for alpha (...-a.png) and beta (...-b.png) 
orbitals will be created. 

Examples:
    
    -a1      : a heat map of the AOs of atom 1 will be created
    -a1,4,5  : heat maps of the AOs of atom 1, 4 & 5 will be created
    
    -cCu -a1 : not possible if atom 1 is not copper
    

CSV file and -ncsv (--newcsv) option
------------------------------------
In a first step all information listed under 'LOEWDIN REDUCED ORBITAL POPULATIONS PER MO' will be read,
and written to a large table. The naming scheme is `orca.out.csv`. In subsequent analyses the program
uses this file which makes analyses much faster. For creating a new CSV file, the option `-ncsv` can be used.

If you restart a calculation with different parameters you should always use the `-ncsv` option, otherwise
the program uses a previous `orca.out.csv` which does not agree with the result of the recent calculation.


Known issues
------------
The plot section crashes without notice if a large number of orbitals (~1000) is processed. Plot artifacts
may occur at even lower numbers of orbitals. The text out is not affected.

The program favor an existing `orca.out.csv` over creating a new one. Besides filenames the program
does not check whether the recent ORCA output matches the CSV file. Using the `-ncsv` option (forces the 
program to create a new CSV file) solves the issue.

                                                                                              
Example inputs
--------------
Threshold and constraints are not valid for the first (two) tables (element contributions to orbitals)
and the bar plot(s).

Orbitals from HOMO-10 to HOMO+10 with iron contributions >= 5% will be analyzed: 

    orca_orb.py -t5 -cFe -oh10 my-calc.out
    
Orbitals from 0 to 10 with contributions of atoms 1 & 3 >= 10% will be analyzed:
    
    orca_orb.py -t10 -c1,3 -o0:10 my-calc.out
    
All orbitals with contributions from all elements (or all atoms) >= 4.2% will be analyzed:
    
    orca_orb.py -t4.2 my-calc.out
    
All orbitals with contributions from all elements (or all atoms) >= 5% will be analyzed. Furthermore 
plots of the contributions from AOs of atom 0 and 1 in all orbitals will be created:
    
    orca_orb.py -t5 -a0,1 my-calc.out
    
 
Have fun!


#### Check https://github.com/radi0sus for updates.

 
BSD 3-Clause License

Copyright (c) 2019, Sebastian Dechert
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''

import os     as ops # for file checking
import glob          # for file checking

import argparse      # argument parser
import re            # regex
import pandas as pd  # pandas tables
import seaborn as sns; sns.set(context='paper',font_scale=0.7) # for the plots
import matplotlib.pyplot as plt                                # for the plots


# do not truncate tables
pd.set_option('display.max_columns',9)
pd.set_option('display.width',1000)
pd.set_option('display.max_rows',None)


# tidy up plots
# delete all previous plots
if ops.path.exists('el-cntrb-a.png'):
    ops.remove('el-cntrb-a.png')
    
if ops.path.exists('el-cntrb-b.png'):
    ops.remove('el-cntrb-b.png')

if ops.path.exists('a-cntrb-a.png'):
    ops.remove('a-cntrb-a.png')
    
if ops.path.exists('a-cntrb-b.png'):
    ops.remove('a-cntrb-b.png')
    
if glob.glob('ao-cntrb-*-a.png'):
    for pngfiles in glob.glob('ao-cntrb-*-a.png'):
        ops.remove(pngfiles)

if glob.glob('ao-cntrb-*-b.png'):
    for pngfiles in glob.glob('ao-cntrb-*-b.png'):
        ops.remove(pngfiles)


# check threshold from argparse
def threshold_check(string):
    value = float(string)
    if value < 0 or value > 100: 
        raise argparse.ArgumentTypeError(f"{value}% exceeds range. Quit." )
    return value


# variables - probably not all of them are necessary - some of them are just reminders
loewdin_last = False            # for detecting the last occurence of look_for_loewdin
look_for_loewdin = 'LOEWDIN REDUCED ORBITAL POPULATIONS PER MO'
is_empty_line = False           # empty line bool in orbital table creation
emptyline = re.compile('^\s*$') # empty line detect in orbital table creation
emptyline_count = 0             # empty line count in orbital table creation
raworbitals = []                # raworbitals reset
first_time = False              # for data frame initialization
spin=0                          # bool if beta orbitals are present
old_csv=0                       # old csv detected in folder
heatmap_ano=True                # for heat map annotations
constr_for_atoms_set=False      # for telling the plot section to plot the AOs of the selected atom
hm_ano_font_size = 4            # font size for heat maps
# end variables

# parse arguments
parser = argparse.ArgumentParser(prog='orca_orb', 
                                 description='Analyze '+look_for_loewdin+'.\n'
                                 '---------------------------------------------------\n'
                                 'Summation of single contributions of elements, atoms, and AOs '
                                 'for a range of given orbitals.\n'
                                 'Saves the result of the analysis in o-analysis.txt.\n'
                                 'Writes a CSV file with orbitals to disk, ' 
                                 'for faster subsequent analyses.',
                                 formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("filename", help="the ORCA output file")

parser.add_argument('-o','--orbitals',
        default='all',
        help='specify orbital(s)\n'
        'e.g. -o5            = analyze orbital 5\n'
        'e.g. -o1-10         = analyze orbitals 1 to 10\n'
        'e.g. -oh (or oHOMO) = analyze the HOMO\n'
        'e.g. -oh4           = analyze orbitals from HOMO-4 to HOMO+4\n')

parser.add_argument('-t','--threshold', type=threshold_check,
        default=0,
        help='specify threshold (in %%) for printing\n'
        'A given threshold can be valid for different summations!\n'
        'orbitals >= threshold will be printed\n'
        'e.g. -t5.2 = analyze orbitals with a contribution of >= 5.2%%')

parser.add_argument('-c','--constraints',
        default='none',
        help='specify elements or(!) atoms for analysis\n'
        'e.g. -cC   = analyze all orbitals that contain contributions from C atoms\n'
        'e.g. -cC,N = analyze all orbitals that that contain contributions from C & N atoms\n'
        'e.g. -c1   = analyze all orbitals that contain contributions from atom 1\n'
        'e.g. -c1,2 = analyze all orbitals that contain contributions from atom 1 & 2\n'
        'e.g. -c1,N = not possible! only contributions from atom 1 will be considered\n'
        'input is case sensitive\n')

parser.add_argument('-a','--aorbitals',
        default='none',
        help='specify atoms for atomic orbitals heat map plots\n'
        'e.g. -a1   = plot heat map of contributions from AOs of atom 1\n'
        'e.g. -a1,2 = plot heat map of contributions from AOs of atom 1 & 2\n')

parser.add_argument('-ncsv','--newcsv',
        default=0, action='store_true',
        help='build new CSV file with orbitals\n')
        
args = parser.parse_args()

threshold=float(args.threshold)

# open orca output file
with open(args.filename,'r') as orca_out_file_name:
        orca_out = orca_out_file_name.readlines()
        #orca_out_file_name.close()  

# search for occurrences of LOEWDIN REDUCED ORBITAL POPULATIONS PER MO   
# keep line number of last occurrence
for i,line in enumerate(orca_out):  
    if look_for_loewdin in line: 
        loewdin_last=i

# end script if LOEWDIN REDUCED ORBITAL POPULATIONS PER MO is not in out file 
# print error message
if loewdin_last is False:  
    print("\n",look_for_loewdin,"not found in '"
          + orca_out_file_name.name+"'.")
    exit()
 
###############################################################################
# most important section
# read orbitals in table oall
# save orbitals as .csv 
# open csv file with orbitals if available (faster analysis)

# check for csv file and read into data frame if available
if ops.path.isfile(args.filename+'.csv') == True:
    
    print('\nFound '+args.filename+'.csv in folder.')
    
    if args.newcsv !=0:
        print('\n-ncsv option active. Building new '+args.filename+'.csv.')
        
    if args.newcsv == 0:
        oall=pd.read_csv(args.filename+'.csv')  # load csv file
        old_csv=1                               # set to 1 if successsful
        # check for beta orbitals in the csv file
        if len(oall[(oall.orb_spin > 0)]):
            spin=1                             # set to 1 if found
    else:
        old_csv=0
        
print('\nReading orbitals from file.\n') 

# no csv file with orbitals = make new one
if old_csv == 0: 
    
    for line in orca_out[loewdin_last+1:]:    

        if "SPIN DOWN" in line: # check for beta orbitals
            spin=1              # set to 1 if found
            
        if not "--" in line and not "SPIN" in line and not "THRESHOLD" in line:
            
            if emptyline.match(line):
  
                if raworbitals:
                    en=pd.DataFrame(raworbitals[0:3]) # orb_no, energy, occ
                    oc=pd.DataFrame(raworbitals[3:])  # atom_no, element, orbital, contribution
                    ob=pd.DataFrame(dict(atom_no=oc[0],element=oc[1],orbital=oc[2]))
                    
                    for i in range(0,len(en.loc[0])):
                        ob.insert(loc=3,column='orb_comp',value=oc[3+i])    # insert contribution
                        ob.insert(loc=0,column='orb_num',value=en.loc[0,i]) # insert orb_no
                        ob.insert(loc=1,column='orb_spin',value=spin)       # insert orb_spin
                        ob.insert(loc=2,column='orb_en',value=en.loc[1,i])  # insert orb_en
                        ob.insert(loc=3,column='orb_occ',value=en.loc[2,i]) # insert occ
                        
                        if i==0:
                            os=pd.DataFrame(ob)                # initialize DataFrame for os
                        else:
                            os=os.append(ob,ignore_index=True) # final table from block
                            
                        # delete rows that will be replaced by the next insertion
                        ob=ob.drop(columns=['orb_num','orb_spin','orb_en','orb_occ','orb_comp'])
                        
                emptyline_count +=1      # 1 empty line = end of the small orbital block
                
                if emptyline_count == 2: # 2 empty lines = end of the whole orbital block
                   break                 # exit the loop
                   
                if first_time == False:
                     oall=pd.DataFrame(os) # initialize DataFrame for oall
                     first_time=True       # but only once
                     
                else:
                    oall=oall.append(os,ignore_index=True)  # combine single block tables to a big table
                raworbitals=[]                              # reset list of lines
                
            else:
                emptyline_count = 0 # reset empty line counter
                
            if emptyline_count == 0: 
                raworbitals.append(line.strip().split()) # split line in words
    
    # assign dtypes to columns (not for str)
    oall['orb_num']=oall.orb_num.astype('int64')
    oall['orb_en']=oall.orb_en.astype('float64')   
    oall['orb_occ']=oall.orb_occ.astype('float32') 
    oall['atom_no']=oall.atom_no.astype('int64')
    oall['orb_comp']=oall.orb_comp.astype('float64')  
    
    # insert reduced orbital description (s,p,d) row in data frame
    oall.insert(loc=6,column='orb_red',value=oall.apply(lambda row: row.orbital[0],axis=1))

# write data frame as csv file to hd
if ops.path.isfile(args.filename+'.csv') == False or args.newcsv !=0:
    
    oall.to_csv(args.filename+'.csv')
    print('Data frame saved to disk as '+args.filename+'.csv\n')

###############################################################################
# get total number of orbitals (alpha & beta)
tot_num_of_orb=oall.groupby(['orb_spin'], as_index=False)['orb_num'].max()
tot_num_of_orb_a=tot_num_of_orb.loc[0,'orb_num']

if spin==1:
    tot_num_of_orb_b=tot_num_of_orb.loc[1,'orb_num'] # beta orbitals
    
# get orbital no of the HOMO
homo_num = oall.groupby(['orb_occ'], as_index=False)['orb_num'].max()
homo_num = homo_num.loc[1,'orb_num']

###############################################################################
# get the numbers of orbitals to process (from argparse) 
# get the constraints (from argparse) 

orbrange = re.compile('\d+')            # regex for orbital range input
orbrange_homo = re.compile('h(\d+)')    # regex for HOMO+-n range input
elm = re.compile('[A-Z][a-z]{0,1}')     # regex for elements: C, N, Fe, ...
atm = re.compile('[\d]+')               # regex for atoms: 0, 1, 2, ...

if args.orbitals == 'all':   
    orb_start = 0
    orb_end = tot_num_of_orb_a
    print(f'Analyzing all orbitals ({orb_start}...{orb_end}).\n')
    
elif args.orbitals == 'HOMO' or args.orbitals == 'h' or args.orbitals == 'homo':  
    orb_start = homo_num
    orb_end = homo_num
    print(f'Analyzing HOMO. Orbital {homo_num}.\n')
    
elif args.orbitals.isdigit():  
    orb_start = int(args.orbitals)
    orb_end = int(args.orbitals)
    print(f'Analyzing orbital {args.orbitals}.\n')
    
elif orbrange.match(args.orbitals):    
    orb_start = int(orbrange.findall(args.orbitals)[0])
    orb_end = int(orbrange.findall(args.orbitals)[1])
    
    if orb_start > orb_end:
        print('Warning! Start orbital > Last orbital. Quit\n')
        exit()
        
    print(f'Analyzing orbitals {orb_start}...{orb_end}.\n')
    
elif orbrange_homo.match(args.orbitals):    
    orb_start = homo_num - int(orbrange_homo.findall(args.orbitals)[0])
    orb_end = homo_num + int(orbrange_homo.findall(args.orbitals)[0])
    print(f'Analyzing orbitals {orb_start}...{orb_end}.\n')
    
else:
    print('Warning! Malformed parameter. Check your input. Quit\n')
    exit()
    
###############################################################################
# get the constraints (from argparse) 
# Element constraints are in the list: list_of_elements
# Atom constraints are in the list: list_of_atoms

if args.constraints == 'none':
        list_of_elements=oall['element'].unique()
        list_of_atoms=oall['atom_no'].unique()
        appl_constr='none' # for print summary

elif elm.match(args.constraints):
    
    if list(set(elm.findall(args.constraints)).intersection(oall['element'].unique())):
        list_of_elements=list(set(elm.findall(args.constraints)).intersection(
                         oall['element'].unique()))
        list_of_atoms=oall['atom_no'].unique()
        appl_constr=f'Elements {list_of_elements}' # for print summary
    else:
        print('Warning! None of the specified elements have been found.\n'
              'Continue using all available elements.\n')
        list_of_elements=oall['element'].unique()
        list_of_atoms=oall['atom_no'].unique()
        appl_constr='none' # for print summary
        
elif atm.match(args.constraints):
    
    if list(set(map(int,atm.findall(args.constraints))).intersection(oall['atom_no'].unique())):
        list_of_atoms=list(set(map(int,atm.findall(args.constraints))).intersection(
                      oall['atom_no'].unique()))
        list_of_elements=oall['element'].unique()
        list_of_atoms_to_display = list_of_atoms
        list_of_atoms_to_display.sort()
        appl_constr=f'Atoms {list_of_atoms_to_display}'
    else:
        print('Warning! None of the specified atoms have been found.\n'
              'Continue using all available atoms.\n')
        list_of_atoms=oall['atom_no'].unique()
        list_of_elements=oall['element'].unique()
        appl_constr='none' # for print summary
        
else: 
    print('Warning! None of the specified elements or atoms have been found.\n'
          'Continue using all available elements and atoms.\n')
    list_of_atoms=oall['atom_no'].unique()
    list_of_elements=oall['element'].unique()
    appl_constr='none' # for print summary

###############################################################################
# get the atomic orbitals (from argparse) 
# Selected atoms are in the list: list_of_atoms_ao

if args.aorbitals == 'none':
        constr_for_atoms_set=False  # tell the plot section not to plot the AOs of the selected atom
        sel_atom_ao='none'          # for print summary
         
if atm.match(args.aorbitals):
    
    # check if the selected atom is in the data frame oall
    if list(set(map(int,atm.findall(args.aorbitals))).intersection(oall['atom_no'].unique())):
        list_of_atoms_ao=list(set(map(int,atm.findall(args.aorbitals))).intersection(
                         oall['atom_no'].unique()))
        
        # check if list matches with constraints of atoms
        if bool(set(list_of_atoms_ao).intersection(list_of_atoms)): 
            list_of_atoms_ao=set(list_of_atoms_ao).intersection(list_of_atoms) # take intersection of both lists
            sel_atom_ao=f'{list_of_atoms_ao}'   # for print summary
            constr_for_atoms_set=True           # tell the plot section to plot the AOs of the selected atom
            
        # check if list matches with constraints of elements
        # elements must be transformed to atom numbers for comparison
        if bool(set(list_of_atoms_ao).intersection(oall.loc[oall['element'].isin(list_of_elements),['atom_no']]['atom_no'])):
            # take intersection of both lists
            list_of_atoms_ao=set(list_of_atoms_ao).intersection(oall.loc[oall['element'].isin(list_of_elements),['atom_no']]['atom_no']) 
            # this has to be here again, to prevent atoms from the element list beeing recognized
            if bool(set(list_of_atoms_ao).intersection(list_of_atoms)):
                sel_atom_ao=f'{list_of_atoms_ao}'  # for print summary
                constr_for_atoms_set=True          # tell the plot section to plot the AOs of the selected atom
            else:
                print('Warning! None of the specified atoms have been found.\n'
                      'No heat map plots of AO contributions of atoms to orbital will be created.\n')
                sel_atom_ao='none'
                constr_for_atoms_set=False
        else:
            print('Warning! None of the specified atoms have been found.\n'
                  'No heat map plots of AO contributions of atoms to orbital will be created.\n')
            sel_atom_ao='none'
            constr_for_atoms_set=False 
            
    else:
        print('Warning! None of the specified atoms have been found.\n'
              'No heat map plots of AO contributions of atoms to orbital will be created.\n')
        sel_atom_ao='none'
        constr_for_atoms_set=False 

else: 
    #print('Warning! None of the specified atoms have been found.\n'
    #      'No heat map plots of AO contributions of atoms to orbital will be created.\n')
    sel_atom_ao='none'
    constr_for_atoms_set=False
     
# error message if range of orbitals is exceeded
if orb_start < 0 or orb_end < 0 or orb_end > tot_num_of_orb_a:
    print(f'Warning! Value exceeds range of orbitals: 0...{tot_num_of_orb_a}. Quit\n')
    exit()

###############################################################################
# output section 
# print summary
# name of the output file is 'o-analysis.txt'
file = open('o-analysis.txt','w')  # open file
    
file.write('==================================================================\n')
file.write(' '.join((look_for_loewdin,'analysis of',args.filename+'\n')))

if orb_start == orb_end:
    file.write(f'Analyzed orbital          : {orb_start}\n')
    
else:
    file.write(f'Analyzed orbitals         : {orb_start}...{orb_end}\n')
    
if spin==1:
    file.write(' '.join(("Alpha spin orbitals       :",str(tot_num_of_orb_a)+'\n')))
    file.write(' '.join(("Beta spin Orbitals        :",str(tot_num_of_orb_b)+'\n')))

else:
    file.write(' '.join(("Number of orbitals        :",str(tot_num_of_orb_a)+'\n')))
    
file.write(' '.join(("Orbital no. of the HOMO   :", str(homo_num)+'\n')))
file.write(' '.join(("Threshold for printing (%):", str(threshold)+'\n')))
file.write("Applied constraints       : " +appl_constr.translate({ord(c): None for c in "[]',"})+"\n")
file.write("Atoms for AO heat maps    : " +sel_atom_ao.translate({ord(c): None for c in "{}[]',"})+"\n")
file.write('==================================================================\n')

###############################################################################
# print orbitals in a given range with a given threshold
# sum over elements (no threshold & no restraints)
# sum over atoms, print  >= threshold (element & atom restraints are applied)
# sum over AOs, print    >= threshold (element & atom restraints are applied)
# AOs in orbitals, print >= threshold (element & atom restraints are applied)
# 

# rename columns
oall=oall.rename({'orb_num':'OrbNo','orb_spin':'Spin','orb_en':'OrbitalEnergy',
                  'orb_occ':'Occupation','atom_no':'AtomNo','element':'Element',
                  'orb_red':'Orb','orbital':'OrbOr','orb_comp':'Cntrb'},
                  axis='columns')

# print '(alpha)' in case of open shell or '' in case of closed shell
if spin==1:
    alpha_str=' (alpha)'
    
else:
    alpha_str=''

# write tables to file:
############################################################################### 
file.write('\nSummary of element contributions (>= 0%) to orbitals'+alpha_str+':\n'
           '==================================================================\n')

sum_by_el_a=oall[(oall.Spin == 0) & (oall.OrbNo >= orb_start)  & (oall.OrbNo <=orb_end) 
            ].groupby(['OrbNo','OrbitalEnergy','Occupation','Element']).agg({'Cntrb':'sum'})

file.write(sum_by_el_a.reset_index().set_index(['OrbNo','OrbitalEnergy','Occupation','Element'])
           .unstack().fillna(0).to_string(index=True)+'\n')

if spin==1:
    file.write('\nSummary of element contributions (>= 0%) to orbitals (beta):\n'
               '==================================================================\n')
    
    sum_by_el_b=oall[(oall.Spin == 1) & (oall.OrbNo >= orb_start)  & (oall.OrbNo <=orb_end) 
                ].groupby(['OrbNo','OrbitalEnergy','Occupation','Element']).agg({'Cntrb':'sum'})
    
    file.write(sum_by_el_b.reset_index().set_index(['OrbNo','OrbitalEnergy','Occupation','Element'])
               .unstack().fillna(0).to_string(index=True)+'\n')
    
###############################################################################  
    
file.write(f'\nSummary of atom contributions (>= {threshold}%) to orbitals'+alpha_str+':\n'
            '==================================================================\n')

sum_by_at_a=oall[(oall.Spin == 0) & (oall.OrbNo >= orb_start)  & (oall.OrbNo <=orb_end) &
            oall.Element.isin(list_of_elements) & oall.AtomNo.isin(list_of_atoms)].groupby(
            ['OrbNo','OrbitalEnergy','Occupation','Element','AtomNo']).agg({'Cntrb':'sum'})

file.write(sum_by_at_a[(sum_by_at_a.Cntrb >= threshold)].to_string(index=True)+'\n')

if spin==1:
    file.write(f'\nSummary of atom contributions (>= {threshold}%) to orbitals (beta):\n'
                '==================================================================\n')
    
    sum_by_at_b=oall[(oall.Spin == 1) & (oall.OrbNo >= orb_start)  & (oall.OrbNo <=orb_end) &
                oall.Element.isin(list_of_elements) & oall.AtomNo.isin(list_of_atoms)].groupby(
                ['OrbNo','OrbitalEnergy','Occupation','Element','AtomNo']).agg({'Cntrb':'sum'})
    
    file.write(sum_by_at_b[(sum_by_at_b.Cntrb >= threshold)].to_string(index=True)+'\n')
    
###############################################################################
    
file.write(f'\nSummary of red. AO contributions (>= {threshold}%) to orbitals'+alpha_str+':\n'
            '==================================================================\n')

sum_by_orb=oall[(oall.Spin == 0) & (oall.OrbNo >= orb_start)  & (oall.OrbNo <=orb_end) &
           oall.Element.isin(list_of_elements) & oall.AtomNo.isin(list_of_atoms)].groupby(
           ['OrbNo','OrbitalEnergy','Occupation','Element','AtomNo','Orb']).agg({'Cntrb':'sum'})

file.write(sum_by_orb[(sum_by_orb.Cntrb >= threshold)].to_string(index=True)+'\n')

if spin==1:
    file.write(f'\nSummary of red. AO contributions (>= {threshold}%) to orbitals (beta):\n'
                '==================================================================\n')
    
    sum_by_orb=oall[(oall.Spin == 1) & (oall.OrbNo >= orb_start)  & (oall.OrbNo <=orb_end) &
               oall.Element.isin(list_of_elements) & oall.AtomNo.isin(list_of_atoms)].groupby(
               ['OrbNo','OrbitalEnergy','Occupation','Element','AtomNo','Orb']).agg({'Cntrb':'sum'})
    
    file.write(sum_by_orb[(sum_by_orb.Cntrb >= threshold)].to_string(index=True)+'\n')
    
###############################################################################
    
file.write(f'\nSummary of AO contributions (>= {threshold}%) to orbitals'+alpha_str+':\n'
            '==================================================================\n')

sum_by_orb_or_a=oall[(oall.Spin == 0) & (oall.OrbNo >= orb_start)  & (oall.OrbNo <=orb_end) &
                oall.Element.isin(list_of_elements) & oall.AtomNo.isin(list_of_atoms)].groupby(
                ['OrbNo','OrbitalEnergy','Occupation','Element','AtomNo','Orb','OrbOr']).agg({'Cntrb':'sum'})

file.write(sum_by_orb_or_a[(sum_by_orb_or_a.Cntrb >= threshold)].to_string(index=True)+'\n')

if spin==1:
    file.write(f'\nSummary of AO contributions (>= {threshold}%) to orbitals (beta):\n'
                '==================================================================\n')
    
    sum_by_orb_or_b=oall[(oall.Spin == 1) & (oall.OrbNo >= orb_start)  & (oall.OrbNo <=orb_end) &
                    oall.Element.isin(list_of_elements) & oall.AtomNo.isin(list_of_atoms)].groupby(
                    ['OrbNo','OrbitalEnergy','Occupation','Element','AtomNo','Orb','OrbOr']).agg({'Cntrb':'sum'})
    
    file.write(sum_by_orb_or_b[(sum_by_orb_or_b.Cntrb >= threshold)].to_string(index=True)+'\n')
    
###############################################################################
    
file.write(f'\nAOs (contribution >= {threshold}%) in orbitals'+alpha_str+':\n'
            '==================================================================\n')

ao_in_orb_a=sum_by_orb_or_a.reset_index().drop(columns=['OrbitalEnergy']).rename(
            {'Occupation':'Occ'},axis='columns').set_index([
            'AtomNo','Element','Orb','OrbOr','OrbNo','Occ']).sort_index()

#ao_in_orb_a=ao_in_orb_a.rename({'Occupation':'Occ'},axis='index')

file.write(ao_in_orb_a[(ao_in_orb_a.Cntrb >= threshold)].to_string(index=True)+'\n')

if spin==1:
    file.write(f'\nAOs (contribution >= {threshold}%) in orbitals (beta):\n'
                '==================================================================\n')
    
    ao_in_orb_b=sum_by_orb_or_b.reset_index().drop(columns=['OrbitalEnergy']).rename(
                {'Occupation':'Occ'},axis='columns').set_index([
                'AtomNo','Element','Orb','OrbOr','OrbNo','Occ']).sort_index() 
        
    #ao_in_orb_b=ao_in_orb_b.rename({'Occupation':'Occ'},axis='index')
    
    file.write(ao_in_orb_b[(ao_in_orb_b.Cntrb >= threshold)].to_string(index=True)+'\n')

file.close() # close file

###############################################################################
# plot section
# 
# plot of element contributions in orbitals (no threshold)
# el-cntrb-a.png & el-cntrb-b.png (if open shell)
# plot of atom contributions in orbitals >= threshold
# a-cntrb-a.png & a-cntrb-b.png (if open shell)

print('Preparing plots.\n')

# unstack table
sum_by_el_plot_a=sum_by_el_a.reset_index().drop(columns=['OrbitalEnergy']).set_index(
                 ['OrbNo','Occupation','Element']).unstack().fillna(0)

# print warning if output gets "unreadable"
if len(sum_by_el_plot_a) > 50:
    print('Warning! A large number of orbitals may reduce the readability of the diagrams.\n')

if spin==1:
    # unstack table
    sum_by_el_plot_b=sum_by_el_b.reset_index().drop(columns=['OrbitalEnergy']).set_index(
                     ['OrbNo','Occupation','Element']).unstack().fillna(0)
    
    # plot options for beta orbitals start here:
    ax=sum_by_el_plot_b.plot.barh(xlim=(0,100),stacked=True) 
    ax.legend(sum_by_el_plot_b.columns.get_level_values(1),loc='upper left')
    ax.set_title('Element contributions (>= 0%) to orbitals (beta).' 
                  f'The orbital number of the HOMO (alpha) is {homo_num}.')
    ax.set_xlabel('Element contribution (%)')
    ax.set_ylabel('(Orbital No., Occupation)')
    
    # reduce some labels in large plots
    if len(sum_by_el_plot_b) > 30:
        ax.set_yticklabels([t if not i%2 else "" for i,t in enumerate(ax.get_yticklabels())])
        
    if len(sum_by_el_plot_b) > 50:
        ax.set_yticklabels([t if not i%4 else "" for i,t in enumerate(ax.get_yticklabels())])
        
    fig = ax.get_figure()
    
    # for very large plots of element contributions
    if len(sum_by_el_plot_b) > 100:
        
       w, h=fig.get_size_inches()
       h = len(sum_by_el_plot_b)/10+1
       fig.set_size_inches(1.5*h, h)
       
       for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
           item.set_fontsize(20)
           
       ax.legend(sum_by_el_plot_b.columns.get_level_values(1),loc='upper left',fontsize=20)
      
    plt.tight_layout()
    fig.savefig('el-cntrb-b.png',dpi=300)
    plt.close(fig)
# plot options for (alpha) orbitals start here:
ax=sum_by_el_plot_a.plot.barh(xlim=(0,100),stacked=True)
ax.legend(sum_by_el_plot_a.columns.get_level_values(1),loc='upper left')
ax.set_title('Element contributions (>= 0%) to orbitals'+alpha_str+'.'
             +f' The orbital number of the HOMO is {homo_num}.')
ax.set_xlabel('Element contribution (%)')
ax.set_ylabel('(Orbital No., Occupation)')

# reduce some labels in large plots
if len(sum_by_el_plot_a) > 30:
    ax.set_yticklabels([t if not i%2 else "" for i,t in enumerate(ax.get_yticklabels())])
    
if len(sum_by_el_plot_a) > 50:
    ax.set_yticklabels([t if not i%4 else "" for i,t in enumerate(ax.get_yticklabels())])
    
fig = ax.get_figure()

# for very large plots of element contributions
if len(sum_by_el_plot_a) > 100:
    
    w, h=fig.get_size_inches()
    h = len(sum_by_el_plot_a)/10+1
    fig.set_size_inches(1.5*h, h)
    
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(20)
        
    ax.legend(sum_by_el_plot_a.columns.get_level_values(1),loc='upper left',fontsize=20)
    
plt.tight_layout()
fig.savefig('el-cntrb-a.png',dpi=300)
plt.close(fig)

###############################################################################
# heat maps

# only if contribution is non-zero
if len(sum_by_at_a[(sum_by_at_a.Cntrb >= threshold)]) != 0:

    # plot of atom contributions in orbitals >= threshold
    sum_by_at_plot_a=sum_by_at_a[(sum_by_at_a.Cntrb >= threshold)].reset_index().drop(columns=['OrbitalEnergy'])
    
    # convert AtomNo to string with leading zero
    sum_by_at_plot_a['AtomNo']=sum_by_at_plot_a['AtomNo'].apply(lambda x: str(x).zfill(2))
    
    # join AtomNo Element to AtomNo-Element
    # otherwise sorting on x-axis is not nice
    sum_by_at_plot_a['Atom'] = sum_by_at_plot_a[['AtomNo','Element']].apply(lambda x: ' '.join(x), axis=1)
    
    # drop 'AtomNo' & 'Element' columns, since no longer needed
    sum_by_at_plot_a=sum_by_at_plot_a.drop(columns=['AtomNo','Element'])
    
    # unstack table
    sum_by_at_plot_a=sum_by_at_plot_a.set_index(['OrbNo','Occupation','Atom']).unstack().fillna(0)
    
    # drop one index level
    sum_by_at_plot_a.columns=sum_by_at_plot_a.columns.droplevel()
    
    # heat map annotations off for large size plots
    if  sum_by_at_plot_a.size > 300:
        print('Heat map annotations for atom contributions to orbitals are turned off.\n')
        heatmap_ano=False # no annotations 

    # plot options for (alpha) orbitals start here:
    ax=sns.heatmap(data=sum_by_at_plot_a,cmap='hot',linecolor='black',
       annot=heatmap_ano,fmt='g',xticklabels=True,linewidths=0.5,cbar=False,annot_kws={"size": hm_ano_font_size}) 
    
    ax.invert_yaxis()
    ax.set_title(f'Atom contributions (>= {threshold}%) to orbitals'+alpha_str+f'. The orbital number of the HOMO is {homo_num}.\n'
                 f'Applied constraints: '+appl_constr.translate({ord(c): None for c in "[]',"})+'\n'
                 f'Contributions <= {threshold}% are "0" or "black" in the heat map.')
    ax.set_xlabel('Atom No.')
    ax.set_ylabel('Orbital No.-Occupation')
    
    fig = ax.get_figure()
    plt.xticks(rotation=90) 
    plt.yticks(rotation=0) 
    fig.tight_layout()
    fig.savefig('a-cntrb-a.png',dpi=300)
    plt.close(fig)

if spin == 1:
    # more or less same as above
    if len(sum_by_at_b[(sum_by_at_b.Cntrb >= threshold)]) != 0:
            
        sum_by_at_plot_b=sum_by_at_b[(sum_by_at_b.Cntrb >= threshold)].reset_index().drop(columns=['OrbitalEnergy'])
        sum_by_at_plot_b['AtomNo']=sum_by_at_plot_b['AtomNo'].apply(lambda x: str(x).zfill(2))
        sum_by_at_plot_b['Atom']=sum_by_at_plot_b[['AtomNo','Element']].apply(lambda x: ' '.join(x), axis=1)
        sum_by_at_plot_b=sum_by_at_plot_b.drop(columns=['AtomNo','Element'])
        sum_by_at_plot_b=sum_by_at_plot_b.set_index(['OrbNo','Occupation','Atom']).unstack().fillna(0)
        sum_by_at_plot_b.columns=sum_by_at_plot_b.columns.droplevel()
        
        # plot options for beta orbitals start here:
        ax=sns.heatmap(data=sum_by_at_plot_b,cmap='hot',linecolor='black',
           annot=heatmap_ano,fmt='g',xticklabels=True,linewidths=0.5,cbar=False,annot_kws={"size": hm_ano_font_size}) 
        ax.invert_yaxis()
        ax.set_title(f'Atom contributions (>= {threshold}%) to orbitals (beta). The orbital number of the HOMO (alpha) is {homo_num}.\n'
                     f'Applied constraints: '+appl_constr.translate({ord(c): None for c in "[]',"})+'\n'
                     f'Contributions <= {threshold}% are "0" or "black" in the heat map.')
        ax.set_xlabel('Atom No.')
        ax.set_ylabel('Orbital No.-Occupation')
    
        fig = ax.get_figure()
        plt.xticks(rotation=90) 
        plt.yticks(rotation=0) 
        fig.tight_layout()
        fig.savefig('a-cntrb-b.png',dpi=300)
        plt.close(fig)
 
###############################################################################
# heat maps for AOs in orbitals
# 

if constr_for_atoms_set == True:
    
    ao_in_orb_plot_a=ao_in_orb_a.reset_index().drop(columns=['Orb'])
    # only atoms with  contribution >= threshold and from list 'list_of_atoms_ao' are in the data frame ao_in_orb_plot_a
    ao_in_orb_plot_a=ao_in_orb_plot_a[(ao_in_orb_plot_a.Cntrb >= threshold) & (ao_in_orb_plot_a.AtomNo.isin(list_of_atoms_ao))]
    
    # if the data frame is empty (atom not in 'list_of_atoms_ao' or contribution below threshold) 
    if len(ao_in_orb_plot_a) != 0: 
       
        # combine the columns Element, AtomNo and OrbOr to one column: ElementAtomNo-OrbOr
        ao_in_orb_plot_a['AOs'] = ao_in_orb_plot_a[ao_in_orb_plot_a.AtomNo.isin(list_of_atoms_ao)][[
                                  'Element','AtomNo','OrbOr']].apply(lambda row: (row['Element'] 
                                  + str(row['AtomNo']) + '-' + row['OrbOr']), axis=1)
        
        # create a plot for every atom in list_of_atoms_ao
        for atoms in list_of_atoms_ao:
            # drop some columns
            hm_ao_in_orb_plot_a = ao_in_orb_plot_a[ao_in_orb_plot_a.AtomNo == atoms].drop(columns=['AtomNo','Element','OrbOr'])
            # unstack table
            hm_ao_in_orb_plot_a = hm_ao_in_orb_plot_a.set_index(['OrbNo','Occ','AOs']).unstack().fillna(0)
            # drop level
            hm_ao_in_orb_plot_a.columns = hm_ao_in_orb_plot_a.columns.droplevel()
            
            # a data frame of a single atom in the list 'list_of_atoms_ao' can be empty
            # do not plot if the data frame is empty
            if len(hm_ao_in_orb_plot_a) != 0:
                
                # heat map annotations on if turned off before and DataFrame size is < 200
                if  hm_ao_in_orb_plot_a.size < 300:
                    heatmap_ano=True    # annotations on
                # create the heatmap
                ax=sns.heatmap(hm_ao_in_orb_plot_a,cmap='hot',linecolor='black',annot=heatmap_ano,fmt='g',
                               xticklabels=True,linewidths=0.5,cbar=False,annot_kws={"size": hm_ano_font_size}) 
                
                # plot options for (alpha) orbitals start here:
                ax.invert_yaxis()
                ax.set_title(f'AO contributions (>= {threshold}%) to orbitals'+alpha_str+
                             f'. The orbital number of the HOMO is {homo_num}.\n'
                             f'Contributions <= {threshold}% are "0" or "black" in the heat map.')
                ax.set_xlabel('Atom No.-AO')
                ax.set_ylabel('Orbital No.-Occupation')
                
                fig = ax.get_figure()
                #plt.xticks(rotation=90) 
                plt.yticks(rotation=0) 
                fig.tight_layout()
                atom_name=hm_ao_in_orb_plot_a.columns[0].split('-')[0] # Element-AtomName for file name
                fig.savefig('ao-cntrb-'+atom_name+'-a.png',dpi=300)
                plt.close(fig)
            
    # same for beta orbitals
    if spin == 1:        
        
        ao_in_orb_plot_b=ao_in_orb_b.reset_index().drop(columns=['Orb'])
        ao_in_orb_plot_b=ao_in_orb_plot_b[(ao_in_orb_plot_b.Cntrb >= threshold) & (ao_in_orb_plot_b.AtomNo.isin(list_of_atoms_ao))]
    
        # if the data frame is empty (atom not in 'list_of_atoms_ao' or contribution below threshold) 
        if len(ao_in_orb_plot_b) != 0:
        
            # combine the columns Element, AtomNo and OrbOr to one column: ElementAtomNo-OrbOr
            ao_in_orb_plot_b['AOs'] = ao_in_orb_plot_b[ao_in_orb_plot_b.AtomNo.isin(list_of_atoms_ao)][[
                                      'Element','AtomNo','OrbOr']].apply(lambda row: (row['Element'] 
                                      + str(row['AtomNo']) + '-' + row['OrbOr']), axis=1)
            
            # create a plot for every atom in list_of_atoms_ao
            for atoms in list_of_atoms_ao:
                # drop some columns
                hm_ao_in_orb_plot_b = ao_in_orb_plot_b[ao_in_orb_plot_b.AtomNo == atoms].drop(columns=['AtomNo','Element','OrbOr'])
                # unstack table
                hm_ao_in_orb_plot_b = hm_ao_in_orb_plot_b.set_index(['OrbNo','Occ','AOs']).unstack().fillna(0)
                # drop level
                hm_ao_in_orb_plot_b.columns = hm_ao_in_orb_plot_b.columns.droplevel()
                
                # a data frame of a single atom in the list 'list_of_atoms_ao' can be empty
                # do not plot if the data frame is empty
                if len(hm_ao_in_orb_plot_b) != 0:
                    
                    # heat map annotations on if turned off before and DataFrame size is < 300
                    if  hm_ao_in_orb_plot_b.size < 300:
                        heatmap_ano=True    # annotations on
                    # create the heatmap
                    ax=sns.heatmap(hm_ao_in_orb_plot_b,cmap='hot',linecolor='black',annot=heatmap_ano,fmt='g',
                                   xticklabels=True,linewidths=0.5,cbar=False,annot_kws={"size": hm_ano_font_size}) 
                    
                    # plot options for (beta) orbitals start here:
                    ax.invert_yaxis()
                    ax.set_title(f'AO contributions (>= {threshold}%) to orbitals (beta)'
                                 f'. The orbital number of the HOMO is {homo_num}.\n'
                                 f'Contributions <= {threshold}% are "0" or "black" in the heat map.')
                    ax.set_xlabel('Atom No.-AO')
                    ax.set_ylabel('Orbital No.-Occupation')
                    
                    fig = ax.get_figure()
                    #plt.xticks(rotation=90) 
                    plt.yticks(rotation=0) 
                    fig.tight_layout()
                    atom_name=hm_ao_in_orb_plot_b.columns[0].split('-')[0] # Element-AtomName for file name
                    fig.savefig('ao-cntrb-'+atom_name+'-b.png',dpi=300)
                    plt.close(fig)
