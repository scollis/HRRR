# -*- coding: utf-8 -*-
"""
Created on Wed Jun  4 15:58:05 2014

@author: mattjohnson
"""

def get_netCDF_variables(filename, variablelist = []):
    """
    Accesses a specified netCDF file and recovers specified variables (if variablelist is empty will return all variables)
    returns a list of data arrays,  dimensions and units for each variable in a list with the date of the file.  
    """
    import numpy as np
    import datetime
    from scipy.io import netcdf
    f = netcdf.netcdf_file(filename, 'r')

    if variablelist == []:
        variablelist = f.variables
    
    date = datetime(filename[-19:-15],filename[-15:-13],filename[-13:-11])
    
    data = []
    units = []
    dim = []
    
    for i in range(len(variablelist)):
        data.append(f.variables(variablelist[i]).data)
        units.append(f.variables(variablelist[i]).units)
        dim.append(f.variables(variablelist[i]).dimensions)
        
    return [[data,dim,units],date]