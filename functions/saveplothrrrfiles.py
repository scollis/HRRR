# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 15:13:18 2014

@author: mattjohnson
"""

from matplotlib import pyplot as plt
from matplotlib import colors
import numpy as np
from mpl_toolkits.basemap import Basemap, addcyclic
import pygrib
import os

def saveplothrrrfiles(filename,parameter,fdirectory = os.getcwd()+'/images',imname = 'img1',filetype = '.png',size = (5,5),dpi = 600,hinp='',scaling=1,final_unit = '',vmax=None,vmin=None): #US
    """
    Plots and saves a given HRRR file over a given parameter and height in hPa over the US.  If the height is left blank 
    it will plot the maximum values of the parameter over all locations.  
    
    The scaling, final_unit vmax and vmin parameters allow fine tuning of the plot to make differences more visible.  
    
    A .png file is saved in the folder existing or created that corresponds to fdirectory and named imname.  
    """
    
    if not os.path.exists(fdirectory):
        os.makedirs(fdirectory)

        
    if hinp != '':
        [data,parameterlist,datah,dataloc,units] = read_Hrrr(filename,[parameter])
    else:
        [data,parameterlist,datah,dataloc,units] = read_Hrrr(filename,[parameter],max=True)
    
    
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
    
    
    plt.savefig(fdirectory+'/'+imname+filetype,figsize = size,dpi=dpi)
    
    return (imname+filetype)