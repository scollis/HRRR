# -*- coding: utf-8 -*-
"""
Created on Fri Jun  6 09:35:18 2014

@author: mattjohnson
"""

def HRRR_inventory(in_dir):
    x = gather_hrrr_files(in_dir)
    x = x[0]
    y = [len(x[i]) for i in range(len(x))]
    return y