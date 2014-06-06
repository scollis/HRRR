# -*- coding: utf-8 -*-
"""
Created on Tue Jun  3 13:33:41 2014

@author: mattjohnson
"""


#from pygrib read example

import pygrib
from matplotlib import pyplot as plt
from matplotlib import colors
import numpy as np
from mpl_toolkits.basemap import Basemap, addcyclic

def grb_to_grid(grb_obj):
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
    
#adaption
def readHrrr(filename, parameters = [''],max = False):
    #filename = '/Users/mattjohnson/HRRR/hrrr.3d.201405291100f001.grib2'
      
    myfile = pygrib.open(filename) #issues in script
    parameterlist = ['Geopotential Height','Temperature','Relative humidity','Dew point temperature','Specific humidity','Vertical velocity','U component of wind','V component of wind','Absolute vorticity','Cloud mixing ratio','Cloud Ice','Rain mixing ratio','Snow mixing ratio','Graupel (snow pellets)']    
       
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
    
#grb = myfile.select(name='Cloud mixing ratio')
#grb_cube=grb_to_grid(grb)
#grb_ice = myfile.select(name='Cloud Ice')
#grb_cube_ice=grb_to_grid(grb_ice)
#
#f = plt.figure(figsize=[12,10])
#m = Basemap(llcrnrlon = -130,llcrnrlat = 20, urcrnrlon = -70,
#           urcrnrlat = 52 , projection = 'mill', area_thresh =10000 ,
#           resolution='l')
#x, y = m(lons, lats)
    
    