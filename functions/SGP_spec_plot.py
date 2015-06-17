# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 14:51:46 2014

@author: mattjohnson
"""
def spec_hrrr_plot(directory,parameter,datetimestart = None,datetimeend = None,hinp = None,hour=0,loc = [-97.485,36.605]):
    """
    Plots a given parameter over a given timespan for a given parameter, modelhour, height, location and directory of 
    HRRR files.  Leaving hinp empty will cause it to plot the maximum values over all heights.  
    """
    import numpy as np
    import matplotlib
    import os
    import matplotlib.pyplot as plt
    %matplotlib inline
    
    x = gather_hrrr_files(directory)
    y = np.array(x[0])
    y = y.transpose()
    y = y[hour]
    
    dates = x[1]
    
    if datetimestart == None != datetimeend:
        print 'error datetimestart and datetimeend can only be none if both are'
        return
    elif datetimestart == None:
        startindex = 0
        endindex = len(dates)
    else:
        startindex = dates.index(datetimestart)
        endindex = dates.index(datetimeend) 
    
    values = []
    times = []
    
    y = y[startindex:endindex]
    
    wkdir = os.getcwd()
    os.chdir(directory)
    
    for i in range(len(y)):
        
        if hinp != None:
            info = read_Hrrr_spec_loc(y[i], parameter,loc = [-97.485,36.605], max = False)
            index = info[2].tolist().index(hinp)
            datart = info[0][0]
            datarts = datart[index]
        else:
            info = read_Hrrr_spec_loc(y[i], parameter,loc = [-97.485,36.605], max = True)
            datarts = info[0][0]
        values.append(datarts)
        times.append(x[1][i])
    
    units = info[-1]
    
    plt.plot(times, values)
    
    plt.xlabel('Time')
    plt.ylabel(parameter[0]+units)
    
    os.chdir(wkdir)
    
    return