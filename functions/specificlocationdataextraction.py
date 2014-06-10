# -*- coding: utf-8 -*-
"""
Created on Fri Jun  6 09:43:46 2014

@author: mattjohnson
"""
from matplotlib import pyplot as plt
from matplotlib import colors
import numpy as np
from mpl_toolkits.basemap import Basemap, addcyclic
import pygrib

def read_Hrrr_spec_loc(filename, parameters = [''],loc = [-97.485,36.605], max = False):
    
    """
    With an option for returning just the maximum values of a given list of parameters at a specific location, this 
    function takes in a filename, list of parameters (all parameters if left blank) and returns the ndarray of data, 
    the list of parameters, list of heights in hPa, location in latitude, longitude and the list of units 
    corresponding to each parameter in a list.  
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
        parameterlist = parameters[:]
                
                    
    data = []
    grb = myfile.select(name = parameterlist[0]) 
    grb_cube = grb_to_grid(grb)
    dataloc =  np.array(grb[0].latlons())
    datah = grb_cube['levels']
    units = []
    
    x = abs(dataloc[0]-loc[0])
    y = abs(dataloc[1]-loc[1])
    xy = x+y
    xymin = min(xy.flatten())
    xy2 = xy.flatten().tolist()
    xyflatindex = xy2.index(xymin)
    [ysize,xsize] = dataloc[0].shape
    zsize = len(grb_cube['levels'])
    xyindex = [xyflatindex/xsize, xyflatindex%xsize]
    
        
    for p in parameterlist:
        grb = myfile.select(name = p)
        grb_cube = grb_to_grid(grb)
        if not max:
            newshape = grb_cube['data'].reshape([ysize,xsize,zsize])
            data.append(newshape[xyindex[0]][xyindex[1]][:])
        else:
            newshape = grb_cube['data'].reshape([ysize,xsize,zsize])
            data.append(newshape[xyindex[0]][xyindex[1]][:].max(axis=0))
        units.append(grb_cube['units'])
   
       
    return [data,parameterlist,datah,loc,units]