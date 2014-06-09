# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 11:46:41 2014

@author: mattjohnson
"""
"""
Imports all functions in the functions folder of our project.  As a script
works for any directory, but can only be directly called for import in the 
HRRR directory.  
"""

import os

wkdir = os.getcwd()

directory = wkdir

while "HRRR" in directory:
    os.chdir(os.path.abspath('..'))

dirpath = os.path.abspath("HRRR")

dirpath2 = dirpath+'/functions/'
    
filenames = os.listdir(dirpath2)
    
for name in filenames:
    execfile(dirpath2+'/'+name)

os.chdir(wkdir)
    
    


