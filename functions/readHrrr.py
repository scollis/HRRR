# -*- coding: utf-8 -*-
"""
Created on Tue Jun  3 13:33:41 2014

@author: mattjohnson
"""

from matplotlib import pyplot as plt
from matplotlib import colors
import numpy as np
from mpl_toolkits.basemap import Basemap, addcyclic
import pygrib

def grb_to_grid(grb_obj):
    #from scollis
    """Takes a single grb object containing multiple
    levels. Assumes same time, pressure levels. Compiles to a cube"""
    n_levels = len(grb_obj)
    levels = np.array([grb_element['level'] for grb_element in grb_obj])
    indexes = np.argsort(levels)[::-1] # highest pressure first
    cube = np.zeros([n_levels, grb_obj[0].values.shape[0], grb_obj[1].values.shape[1]])
    for i in range(n_levels):
        cube[i,:,:] = grb_obj[indexes[i]].values
    cube_dict = {'data' : cube, 'units' : grb_obj[0]['units'],
                 'levels' : levels[indexes]}
    return cube_dict
    
def read_Hrrr(filename, parameters = [''],max = False):
    
    """
    With an option for returning just the maximum values of a given list of parameters at each location, this function 
    takes in a filename, list of parameters (all parameters if left blank) and returns the ndarray of data, the list
    of parameters, list of heights in hPa, ndarray of locations and the list of units corresponding to each parameter
    in a list.  
    """
    
    myfile = pygrib.open(filename) 
    parameterlist = ['Geopotential Height','Temperature','Relative humidity','Dew point temperature',
        'Specific humidity','Vertical velocity','U component of wind','V component of wind',
        'Absolute vorticity','Cloud mixing ratio','Cloud Ice','Rain mixing ratio','Snow mixing ratio',
        'Graupel (snow pellets)']    
       
    if parameters != ['']:
        for i in range(len(parameters)):
            x = parameterlist.count(parameters[i])
            if x == 0:                    
                print 'requested parameter not in list'
                print parameters[i]  
                return 0
        parameterlist = parameters[:]
            
                
    data = []
    grb = myfile.select(name = parameterlist[0]) 
    grb_cube = grb_to_grid(grb)
    dataloc =  np.array(grb[0].latlons())
    datah = grb_cube['levels']
    units = []
    
    for p in parameterlist:
        grb = myfile.select(name = p)
        grb_cube = grb_to_grid(grb)
        if not max:
            data.append(grb_cube['data'])
        else:
            data.append(grb_cube['data'].max(axis=0))
        units.append(grb_cube['units'])
    
    return [data,parameterlist,datah,dataloc,units]
    

    
    