# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 11:46:41 2014

@author: mattjohnson
"""

import os

dirpath = os.path.abspath("HRRR")
dirfiles = os.listdir(dirpath)


dirpath2 = dirpath+'/functions/'
    
filenames = os.listdir(dirpath2)
    
for name in filenames:
    execfile(dirpath2+'/'+name)

    
    


