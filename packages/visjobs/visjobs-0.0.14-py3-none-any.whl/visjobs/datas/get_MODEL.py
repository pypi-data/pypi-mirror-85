# -*- coding: utf-8 -*-
#!/usr/bin/env python
# coding: utf-8
import xarray as xr
from datetime import datetime,timedelta
import numpy as np


#learn if the latest wanted or the desired date from user?
def pick_data(year=None, month=None, day=None, hour=None, latest=False, model='GFS', hourly=False, resolution=0.25,
              *args, **kwargs):
    """Returns Xarray Dataset of the relevant atmospheric model data
    
        year       :str;
        month      :str; (eg. Instead of '1' input '01')
        day        :str; (eg. Instead of '1' input '01')
        hour       :str; Options;
                            For GFS, GEFS, NAM: '18', '12', '06', '00' [Should be given]
                            For HRRR, NBM's     : '00', '01', ...., '23' [Should be given]
                            
        latest     :Boolean (If Latest=True given date is no more importance)
        model      :str; Options: 'GFS', 'NAM', 'GEFS', 'HRRR', 'NBM_1HR', 'NBM_3HR', 'NBM_6HR' 
        hourly     :Boolean; (Only valid for GFS, HRRR and NBM_1HR Data):
                                              --> HRRR and NBM_1HR only valid for hourly=True
                                                
        Resolution :float; (Only valid for GFS Data, vomitted for other models)"""
    
    #Check if user has passed a valid obligatory hour
    try:
        if hour != None:
            pass
    except:
        print("""Error --> Even If you indicate Latest=True, please input the run hour..
                               Options:
                                   For GFS, NAM, 'GEFS': '18', '12', '06', '00'
                                   For HRRR, NBM's     : '00', '01', '02' ,......, '23' (Full day)
                  """)
        raise
            
    
    #multiply resolution with 10 (only for GFS)
    resolution = int(np.multiply(resolution,100))
    
    #available models
    models = np.array(['GFS', 'NAM', 'GEFS', 'HRRR',
                       'NBM_1HR', 'NBM_3HR', 'NBM_6HR'])
    
    #available hours
    hours = np.array(['18','12','06','00'])
    
    #check user only inputs hourly and GFS together not any else option 
    if model in ['NAM', 'GEFS', 'NBM_3HR', 'NBM_6HR'] and hourly == True:
        print('Error --> model={} and hourly=True choices can not be done together..'.format(model))
        raise
    
    #if HRRR is choosen the hourly has to be True
    if model in ['HRRR', 'NBM_1HR'] and hourly != True:
        print('Error --> model={} has only hourly=True option !..'.format(model))
        raise
    
    #Checking if user asking for the latest data, or the user indicates a specific date..
    if latest == True:
        
        # get the latest year,month,day
        time = datetime.utcnow()
        year = str(time.year)
        month = time.month
        day=time.day
        if month<10:
            month = str(0)+str(month)
        if day<10:
            day = str(0)+ str(day)
    
    #User should give hour input for latest=True
    if latest == True:
        if hour is None:
            print("""Error --> For latest=True, Please input latest run's hour:
                               You can check latest hour from one of the below links (According to data you want):
                                   http://nomads.ncep.noaa.gov:80/dods/blend/blend{}
                                   http://nomads.ncep.noaa.gov:80/dods/gfs_0p25/gfs{}
                                   http://nomads.ncep.noaa.gov:80/dods/nam/nam{}
                                   http://nomads.ncep.noaa.gov:80/dods/hrrr/hrrr{}
                                   http://nomads.ncep.noaa.gov:80/dods/gens_bc/gens{}""".
                                 format(str(year)+str(month)+str(day),
                                        str(year)+str(month)+str(day),
                                        str(year)+str(month)+str(day),
                                        str(year)+str(month)+str(day),
                                        str(year)+str(month)+str(day),))
                                                
            raise
        else:
            pass
    
    #Check if year,month,day is given for latest=False option
    if latest == False:
        
        
        if year and month and day is not None:
            pass
        
        else:
            print('Error --> Please input year, month and day for latest=False')
            raise
            
        
    #GFS
    if model == models[0]:
        
        if hourly == False:

            data = xr.open_dataset(r'http://nomads.ncep.noaa.gov:80/dods/gfs_0p{}/gfs{}/gfs_0p{}_{}z'.
                                     format(resolution, str(year)+str(month)+str(day), resolution, hour), 
                                     *args, **kwargs)
            print('Addressing Data: ', 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p{}/gfs{}/gfs_0p{}_{}z'.
                                     format(resolution, str(year)+str(month)+str(day), resolution, hour))
            
        elif hourly == True:

            data = xr.open_dataset(r'http://nomads.ncep.noaa.gov:80/dods/gfs_0p{}_1hr/gfs{}/gfs_0p{}_1hr_{}z'.
                                     format(resolution, str(year)+str(month)+str(day), resolution, hour),
                                     *args, **kwargs)
            print('Addressing Data: ', 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p{}_1hr/gfs{}/gfs_0p{}_1hr_{}z'.
                                     format(resolution, str(year)+str(month)+str(day), resolution, hour) )
        
    #NAM
    elif model == models[1]:
        
        data = xr.open_dataset(r'http://nomads.ncep.noaa.gov:80/dods/nam/nam{}/nam_{}z'.
                                 format(str(year)+str(month)+str(day), hour),
                                 *args, **kwargs)
        print('Addressing Data: ', 'http://nomads.ncep.noaa.gov:80/dods/nam/nam{}/nam_{}z'.
                                 format(str(year)+str(month)+str(day), hour) )
        
    #GEFS
    elif model == models[2]:
        
        data = xr.open_dataset(r'http://nomads.ncep.noaa.gov:80/dods/gefs/gefs{}/gefs_pgrb2bp5_all_{}z'.
                                 format(str(year)+str(month)+str(day), hour),
                                 *args, **kwargs)
        print('Addressing Data: ', 'http://nomads.ncep.noaa.gov:80/dods/gefs/gefs{}/gefs_pgrb2bp5_all_{}z'.
                                 format(str(year)+str(month)+str(day), hour) )
        
    #HRRR
    elif model == models[3]:
        
        data = xr.open_dataset(r'http://nomads.ncep.noaa.gov:80/dods/hrrr/hrrr{}/hrrr_sfc.t{}z'.
                                 format(str(year)+str(month)+str(day), hour),
                                 *args, **kwargs)
        print('Addressing Data: ', 'http://nomads.ncep.noaa.gov:80/dods/hrrr/hrrr{}/hrrr_sfc.t{}z'.
                                 format(str(year)+str(month)+str(day), hour) )
        
    #NBM_1HR
    elif model == models[4]:
        
        data = xr.open_dataset(r'http://nomads.ncep.noaa.gov:80/dods/blend/blend{}/blend_1hr_{}z'.
                                 format(str(year)+str(month)+str(day), hour),
                                 *args, **kwargs)
        print('Addressing Data: ', 'http://nomads.ncep.noaa.gov:80/dods/blend/blend{}/blend_1hr_{}z'.
                                 format(str(year)+str(month)+str(day), hour) )
        
    #NBM_3HR
    elif model == models[5]:
        
        data = xr.open_dataset(r'http://nomads.ncep.noaa.gov:80/dods/blend/blend{}/blend_3hr_{}z'.
                                 format(str(year)+str(month)+str(day), hour),
                                 *args, **kwargs)
        print('Addressing Data: ', 'http://nomads.ncep.noaa.gov:80/dods/blend/blend{}/blend_3hr_{}z'.
                                 format(str(year)+str(month)+str(day), hour))
        
    #NBM_6HR
    elif model == models[6]:
        
        data = xr.open_dataset(r'http://nomads.ncep.noaa.gov:80/dods/blend/blend{}/blend_6hr_{}z'.
                                 format(str(year)+str(month)+str(day), hour),
                                 *args, **kwargs)
        
        print('Addressing Data: ', 'http://nomads.ncep.noaa.gov:80/dods/blend/blend{}/blend_6hr_{}z'.
                                     format(str(year)+str(month)+str(day), hour))  
        
    print('Connected {} Data via OpenDAP'.format(model))
    return data

#now with this function we will be able to specify the area we are interested and also the variables.
def pick_area(data ,total_process, interval ,list_of_vars, list_of_areas, init_time=0, pr_height=None, ):
    """ Returns time_with_interval and the dictionary of the areas with variables
     
        data          :str; 'GFS', 'NAM', 'GEFS', or 'HRRR' Xarray DataArray should be given
        total_process :int; means the until which time step data is expected (1 or 2 or 100 etc.)
        interval      :int; means until the expected time step in which interval data should be taken.
        list_of_vars  :list of str; (Data variable names) the list of variables can be also a single element list:
                                    ['tmp2m'] or ['tmp2m', 'hgtprs'] etc.
                                    
        list_of_areas :list of str; the list of areas can be also a single element: 
                                    available options:
                                    ['europe','northamerica','australia','gulfofmexico','carribeans','indianocean']
        pr_height     :If the desired data is in pressure levels, which levels are expected? List of Pressure Levels:
                                    ['500'] or ['1000', '850', '500'] etc.
        
    """
    
    
    
    #trying if the longitude values change from 0 to 360 or -180 to 180?
    
    if data['lon'].values[0] < 0:
        
        p_d = {'europe' : [0, 48, 30, 65],
              'northamerica' : [-142,-42,0,60],
              'australia' : [80,180,-50,10],
              'gulfofmexico' : [-100,-75,18,31],
              'carribeans' : [-85,-60,12,38], 
              'indianocean' : [30, 130,-35,35],
              'NH' : [-180, 180 ,0,90]}
                                                                  
    # -180 to 180 change the values given in the dictionary to relevant
    else:
        
        p_d = {'europe' : [0, 48, 30, 65],
              'northamerica' : [218,318,-10,70],
              'australia' : [80,180,-50,10],
              'gulfofmexico' : [260,285,14,37],
              'carribeans' : [275,300,12,38], 
              'indianocean' : [30, 130,-35,35],
              'NH' : [0, 360 ,0,90]}
        
    
    
    places_dict = {}
    #looping in the list of areas
    say_pl = 1
    for pl in list_of_areas:
        variables_l = {}
        #looping in the list of variables
        say_var =1
        for var in list_of_vars:
            #check if data contains 'lev' coords.
            try:
                
                #wrap the data
                single = data[var].sel(lon=slice(p_d[pl][0],p_d[pl][1]),  
                                       lat=slice(p_d[pl][2],p_d[pl][3]), 
                                       lev=pr_height).isel(time=slice(init_time, total_process, interval))
               
            #if no 'lev' coords exist.
            except:
                single = data[var].sel(lon=slice(p_d[pl][0],p_d[pl][1]),  
                                       lat=slice(p_d[pl][2],p_d[pl][3]),).isel(time=slice(init_time, total_process, interval))
            
                #append a single variable given by the user
            variables_l[var] = single
         
        
        #append all the variables with respect to their area of interest.
        places_dict[pl] = variables_l
    
    #return
    return places_dict