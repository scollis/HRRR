# -*- coding: utf-8 -*-
"""
Created on Mon Jun  2 09:23:00 2014

@author: mattjohnson
"""

class datafileset:
    
    
    import datetime
    import numpy as np
    
    def __init__(self,path):
        self.filesets = []
        self.dates = []
        self.filetype = []
        self.dataname = []
        
        #hrrrfiles
        [hrrrfiles, dates] = gatherHrrrFiles(path)
        
        hrrrfiles = np.array(hrrrfiles) 
        lens = len(hrrrfiles[0])
        newdates = dates[:]
        for i in range(lens):
            for j in range(len(dates)):
                newdates[j] = datetime.datetime(dates[j].year,dates[j].month,dates[j].day,dates[j].hour+i,dates[j].minute) 
        
            temphrrrfiles = [hrrrfiles[j][i] for j in range(len(hrrrfiles))]
            self.combine(temphrrrfiles,newdates) 
            self.filetype.append('hrrr')
            self.dataname.append('hrrr'+str(i))
        
            "..."
        
    def combine(self,files,dates):
        if self.filesets == []:
            self.filesets = [[files[i]] for i in range(len(files))]
            self.dates = dates[:]
            return
        else:
            for i in range(len(files)):
                if self.dates.count(dates[i]) > 0:
                    self.filesets[self.dates.index(dates[i])].append(files[i])
                else:
                    j = 0
                    size = len(self.filesets[0])
                    temparray = [None for k in range(size)]
                    temparray.append(files[i])
                    if dates[i]>self.dates[len(dates)-1]:
                        self.dates.append(dates[i])
                        self.filesets.append(temparray) 
                        continue
                    while dates[i]>self.dates[j]:
                        j = j+1
                        
                    self.dates.insert(j,dates[i])
                    self.filesets.insert(j,temparray)
            lengths = [len(self.filesets[i]) for i in range(len(self.filesets))]
            maxlength = max(lengths)
            for i in range(len(self.filesets)):
                for j in range(maxlength-lengths[i]):
                    self.filesets[i].append(None)
    
    
    def accessfilelist(self,date):
        if self.dates.count(date)>0:
            index = self.dates.index(date)
            filelist = self.filesets[index]
            return filelist
        else:
            print 'invalid date input'
            return
            
    def readdata(self):
        values = [[] for k in range(len(self.dates))]
        for j in range(len(self.dates)):
            files = self.accessfilelist(self.dates[j])
            for i in range(len(self.filetype)):
                fcn = 'read'+self.filetype[i]+'('+'files'+')'
                values[j].append(eval(fcn))
                
        return values        
                
                
    
        
        
    
    
                
    
            
            
            
        
        
        