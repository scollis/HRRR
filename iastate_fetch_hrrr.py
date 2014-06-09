#!/usr/bin/env python
#Fetch grb files from ia state website.
import sys, os, urllib, urllib2

def fetch_HRRR(forecast_time = 'f000', dimensionality = '3d', outdir = '/data/HRRR/'):
    HRRR_url = 'http://hrrr.agron.iastate.edu/data/hrrr/'
    all_files = urllib.urlopen(HRRR_url).read()
    all_times = []
    for item in all_files.split("\n"):
        if "a href" in item:
            idx = item.find('a href="')
            all_times.append(item[idx + 8 : idx + 20])
    last_dir = HRRR_url + all_times[-1]
    print last_dir
    filename = 'hrrr.' + dimensionality + '.' + all_times[-1] + forecast_time + '.grib2'
    exising_hrrr_files = os.listdir(outdir)
    outfile = outdir + filename
    if filename in exising_hrrr_files:
        print('File exists, saving bandwidth')
    else:
        print('fetching')
        try:    
            req = urllib2.urlopen(last_dir + '/' + filename)
            outobj=open(outfile, 'wb')
            outobj.write(req.read())
            outobj.close()
        except:
            outfile = 'null'
            print('File not found, skipping')
    return outfile

if __name__ == '__main__':
    print('HRRR fetching')
    r_outdir = sys.argv[1]
    n_hours = int(sys.argv[2])
    forecast_str = 'f%(dd)03d'
    f_strs = [forecast_str % {'dd' : k } for k in range(n_hours)]
    print(f_strs)
    fnames = [fetch_HRRR(forecast_time = fs, outdir = r_outdir) for fs in f_strs]
    