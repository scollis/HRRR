# -*- coding: utf-8 -*-
"""
Created on Thu May 29 16:55:37 2014

@author: mattjohnson
"""

def gather_hrrr_files(path, datestrings = [], hourslists = []):
    
    """
    Takes in a string path leading to a set of HRRR files, a list of datetime objects (datestrings) and a list of the same 
    size containing lists of the corresponding model hours requested (hourslists), if datestrings and hourslists are 
    omitted or both empty the output will be for all dates and model hours files available in the path, if datestrings 
    and hourslists are not the same length zero is returned along with an error message.  
    
    The output is a list with the first entry being a list corresponding to each requested date with each entry
    containing a list of the hour filenames requested and the second entry contains the list of datetime objects that
    correspond to each date in the first entry.  The hours are always 0,1,2... While the dates come in the same order as
    they were in datestrings.  If datestrings and hourslists are omitted or both empty the dates and the hours will all
    be sequential. 
    """
    
    import numpy as np
    import matplotlib
    import matplotlib.pyplot as plt
    import os
    import glob
    import matplotlib.dates
    import datetime
    
    if (len(datestrings) != len(hourslists)):
        print 'datetimes and requested hours don\'t correspond (different lengths)'
        return

    files = os.listdir(path) 

    #removing files without correct format
    i = 0
    
    while i < len(files):
        filetemp = files[i]
        if (filetemp[0:8] != 'hrrr.3d.'):
            files.remove(filetemp)
        elif (filetemp[24:30] != '.grib2'):
            files.remove(filetemp)
        else:
            i = i+1

    
    length = len(files)

    if length == 0:
        print 'no available HRRR files'
        return
        
    year =range(length)
    months = range(length)
    hours = range(length)
    days = range(length)
    minutes = range(length)
    modelhours = range(length) 
    
    #Getting the datetime objects and model hours from each file  
    for i in range(length):
            
        tempfile = files[i]
            
        for j in range(6):
            if j==0:
                 year[i] = int(tempfile[8:12])
            elif j==1:
                 months[i] = int(tempfile[12:14])
            elif j==2:
                 days[i] = int(tempfile[14:16])
            elif j==3:
                hours[i] = int(tempfile[16:18])
            elif j==4:
                minutes[i] = int(tempfile[18:20])
            elif j==5:
                modelhours[i] = int(tempfile[21:24])
                      
    datetimes = [datetime.datetime(year[i],months[i],days[i],hours[i],minutes[i]) for i in range(length)]
        
    datenums = matplotlib.dates.date2num(datetimes)
    datenums = datenums.tolist()
    
    #Generating the full datestrings and modelhours if only given path
    if datestrings==[] and hourslists==[]:
        datestrings = datetimes[:]
        datestrings = set(datestrings)
        datestrings = list(datestrings)
        datestrings.sort()
        maxhours = max(modelhours)
        temparray = [None for i in range(maxhours+1)]                
        filelists = [temparray[:] for i in range(len(datestrings))]

        for i in range(len(datetimes)):
                date = datetimes[i]
                hour = modelhours[i]
                index = datestrings.index(date)
                filelists[index][hour] = files[i]
        return [filelists,datestrings]
        
                            
    
    #finding the filenames corresponding to each requested date/time and model hours
    filelists = []
       
    for k in range(len(datestrings)):
        datestring = datestrings[k]
        hours = hourslists[k]
        datenumber = matplotlib.dates.date2num(datestring)
        indexnum = datenums.count(datenumber)
            
        
        indexes3 = []
        indexes2 = []
        datenumstemp = datenums[:]
          
        for i in range(indexnum):  
            aindex = datenumstemp.index(datenumber)
            indexes2.append(aindex+i)
            datenumstemp.remove(datenumber)
            

        modelhourstemp = [modelhours[i] for i in indexes2]
        datefiles = [files[i] for i in indexes2]
        hourstemp = hours
        
        #Checking that requested dates and modelhours exist
        if indexes2 == []:
            print '\nrequested datetime not in path: '
            print datestring
            print '(no files gathered for this date)'
            continue
        
        count = 0
        for i in range(len(hourstemp)):
            for j in range(len(modelhourstemp)):
                if hourstemp[i] == modelhourstemp[j]:
                    count = count+1
                    
        if count<len(hourstemp):
            print '\nat least one requested model hour not in path for:'
            print 'date requested: ' 
            print datestring
            print '(no files gathered for this date)'
            print 'hours requested: '
            print hourstemp
            print 'hours present: '
            print modelhourstemp
            continue
        
        for i in range(len(hourstemp)):
            value = min(hourstemp)
            indexes3.append(modelhourstemp.index(value))
            hourstemp.remove(value)
         
        filelist = [datefiles[i] for i in indexes3]
        filelists.append(filelist)
           
    x = [filelists, datestrings]
    return x
    