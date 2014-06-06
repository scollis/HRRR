# -*- coding: utf-8 -*-
"""
Created on Wed Jun  4 14:03:36 2014

@author: mattjohnson
"""
import pygrib
from matplotlib import pyplot as plt
from matplotlib import colors
import numpy as np
from mpl_toolkits.basemap import Basemap, addcyclic

def plothrrrfromfile(filename,parameter,hinp='',scaling=1,final_unit = '',vmax=None,vmin=None): #US
#    filename = '/Users/mattjohnson/HRRR/hrrr.3d.201405291100f001.grib2'
#    parameter = 'Cloud Ice'
#    hinp = 800 hPa
    if hinp != '':
        [data,parameterlist,datah,dataloc,units] = readHrrr(filename,[parameter])
    else:
        [data,parameterlist,datah,dataloc,units] = readHrrr(filename,[parameter],max=True)
    
    if hinp !='':
        datah = datah.tolist()
        hindex = datah.index(hinp)
    
    if final_unit == '':
        final_unit = units[0]
    
    f = plt.figure(figsize=[12,10])
    m = Basemap(llcrnrlon = -130,llcrnrlat = 20, urcrnrlon = -70,
               urcrnrlat = 52 , projection = 'mill', area_thresh =10000 ,
               resolution='l')
    
    
    x, y = m(dataloc[1],dataloc[0])
    data = np.array(data)
    
    if hinp != '':
        newdata = data[0][hindex][:][:]
    else:
        newdata = data[0]
    
    my_mesh = m.pcolormesh(x, y, newdata*scaling, vmax = vmax,vmin = vmin)
    my_coast = m.drawcoastlines(linewidth=1.25)
    my_states = m.drawstates()
    my_p = m.drawparallels(np.arange(20,80,4),labels=[1,1,0,0])
    my_m = m.drawmeridians(np.arange(-140,-60,4),labels=[0,0,0,1])
    
    plt.colorbar(label=final_unit)
    plt.show()
    
    
