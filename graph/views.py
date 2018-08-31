from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse

from netCDF4 import Dataset, num2date
from scipy import stats

import datetime
import numpy as np
import math

def fetchData(lacation,type_use):
    name_file = lacation
    dataset = Dataset(name_file, 'r')
    keys = dataset.variables.keys()
    dataset_var = dataset.variables
    # print(keys)
    temp_data = {}
    for k in type_use:  
        if not(type_use == "lat" or type_use == "lon" or type_use == "time"):
            temp_data[k] = dataset_var[k][:]
        else:
            temp_data[k] = [temp for temp in dataset_var[k][:]]

    return temp_data

def fetAvgWorldData(indexs):
    # indexs = #nc.variables['Ann'][:]
    annavg = []
    for t in range(0,len(indexs)-1):
        avg = np.average(indexs[t])
        annavg.append(avg)

    return annavg

class DataPlotTXx(View):
    def get(self, request):

        data_list = fetchData('ghcndex_current/GHCND_TXx_1951-2018_RegularGrid_global_2.5x2.5deg_LSmask.nc',["time","Ann","lat","lon"])
        time = data_list["time"]
        AnnUse = data_list["Ann"]
        lat_list = data_list["lat"]
        lon_list = data_list["lon"]

        lat_index = 58
        lon_index = 13

        temp_data = []
        for i ,t in enumerate(time):
            if math.isnan(AnnUse[i][58][13]):
                pass
            else:
                temp_data.append(float("{0:.2f}".format(AnnUse[i][lat_index][lon_index])))
        temp_result = {"time": [int(t) for t in time], "data": temp_data, "lat":lat_list[lat_index] , "lon":lon_list[lon_index]}

        return render(request,'graphTXx.html',{"data":temp_result})

class DataPlotTNx(View):
    def get(self, request):
        data_list = fetchData('ghcndex_current/GHCND_TNx_1951-2018_RegularGrid_global_2.5x2.5deg_LSmask.nc',["time","Ann","lat","lon"])
        time = data_list["time"]
        AnnUse = data_list["Ann"]
        lat_list = data_list["lat"]
        lon_list = data_list["lon"]

        lat_index = 58
        lon_index = 13

        temp_data = []
        for i ,t in enumerate(time):
            if math.isnan(AnnUse[i][58][13]):
                pass
            else:
                temp_data.append(float("{0:.2f}".format(AnnUse[i][58][13])))
        temp_result = {"time": [int(t) for t in time], "data": temp_data, "lat":lat_list[lat_index] , "lon":lon_list[lon_index]}

        return render(request,'graphTNx.html',{"data":temp_result})


class DataPlotWorldTXx(View):
    def get(self, request):
        name_nc = 'ghcndex_current/GHCND_TXx_1951-2018_RegularGrid_global_2.5x2.5deg_LSmask.nc'
        dataset = Dataset(name_nc, 'r')
        time = dataset.variables["time"][:]
        data = fetAvgWorldData(dataset.variables['Ann'][:])

        temp_result = {"time": [int(t) for t in time], "data": data}
        print(temp_result)
        print(len(temp_result["time"]),len(temp_result["data"]))
        return render(request,'graphWorldTXx.html',{"data":temp_result})        

class DataPlotWorldTNx(View):
    def get(self, request):
        name_nc = 'ghcndex_current/GHCND_TNx_1951-2018_RegularGrid_global_2.5x2.5deg_LSmask.nc'
        dataset = Dataset(name_nc, 'r')
        time = dataset.variables["time"][:]
        data = fetAvgWorldData(dataset.variables['Ann'][:])

        temp_result = {"time": [int(t) for t in time], "data": data}
        print(temp_result)
        print(len(temp_result["time"]),len(temp_result["data"]))
        return render(request,'graphWorldTNx.html',{"data":temp_result})        



def fetchRawdata(time_list, data, lat_index, lon_index):
    sum_daily_to_month = 0
    temp_month_data = []
    temp_m = 1
    for i in range(0,len(time_list)):
        if(time_list[i].month == temp_m):
            sum_daily_to_month += data[i][lat_index][lon_index]
        else:
            temp = sum_daily_to_month/int(time_list[i-1].day)
            temp_month_data.append(float("{0:.2f}".format(temp)))
            sum_daily_to_month = data[i][lat_index][lon_index]
            temp_m = time_list[i].month
    
    return temp_month_data


# Graph Location

class Graph_temp_rain(View):
    def get(self, request):
        name_nc_temp = 'ghcndex_current/tmax.2017.nc'
        name_nc_precip = 'ghcndex_current/precip.2017.nc'
        datasettemp = Dataset(name_nc_temp, 'r')
        datasetprecip = Dataset(name_nc_precip, 'r')
        time_list = datasettemp.variables["time"]
        time_list = num2date(time_list[:],time_list.units)
        lat_list = datasettemp["lat"][:]
        lon_list = datasettemp["lon"][:]

        temp = datasettemp.variables['tmax'][:]
        precip =  datasetprecip.variables['precip'][:]

        lat_index = 149
        lon_index = 202

        temp_monly = fetchRawdata(time_list, temp,lat_index, lon_index)
        precip_monly = fetchRawdata(time_list, precip,lat_index, lon_index)
        
        temp_result = {"time": time_list[0].year, "data": {"temp": temp_monly,"precip": precip_monly}, "lat": lat_list[lat_index] ,"lon": lon_list[lon_index]}
        # print(temp_result)
        # print(len(temp_result["time"]),len(temp_result["data"]))
        return render(request,'graphRainfall_temp.html',{"data":temp_result})    

class Graph_temp_max_min(View):
    def get(self, request):

        data_list_TXx = fetchData('ghcndex_current/GHCND_TXx_1951-2018_RegularGrid_global_2.5x2.5deg_LSmask.nc',["time","Ann","lat","lon"])
        data_list_TNx = fetchData('ghcndex_current/GHCND_TNx_1951-2018_RegularGrid_global_2.5x2.5deg_LSmask.nc',["time","Ann","lat","lon"])

        time = data_list_TXx["time"]
        AnnUse = data_list_TXx["Ann"]
        AnnUse_tnx = data_list_TNx["Ann"]
        lat_list = data_list_TXx["lat"]
        lon_list = data_list_TXx["lon"]

        lat_index = 58
        lon_index = 13

        temp_data_max = []
        temp_data_min = []

        for i ,t in enumerate(time):
            if math.isnan(AnnUse_tnx[i][lat_index][lon_index]):
                break   
            else:
                temp_data_max.append(float("{0:.2f}".format(AnnUse[i][lat_index][lon_index])))
                temp_data_min.append(float("{0:.2f}".format(AnnUse_tnx[i][lat_index][lon_index])))
        temp_result = {"time": [int(str(t)[:4]) for t in time], "data": {"max":temp_data_max, "min":temp_data_min}, "lat":lat_list[lat_index] , "lon":lon_list[lon_index]}
        
        return render(request,'Graph_Tmin_Tmax.html',{"data": temp_result})  

class Graph_trend_line(View):
    def get(self, request):

        data_list_TXx = fetchData('ghcndex_current/GHCND_TXx_1951-2018_RegularGrid_global_2.5x2.5deg_LSmask.nc',["time","Ann","lat","lon"])
        
        time = data_list_TXx["time"]
        AnnUse = data_list_TXx["Ann"]
        lat_list = data_list_TXx["lat"]
        lon_list = data_list_TXx["lon"]

        lat_index = 58
        lon_index = 13

        temp_data_max = []
        temp_data_min = []

        time_use = []

        for i ,t in enumerate(time):
            if math.isnan(AnnUse[i][lat_index][lon_index]):
                break   
            else:
                temp_data_max.append(float("{0:.2f}".format(AnnUse[i][lat_index][lon_index])))
                time_use.append(int(str(time[i])[:4]))
        
        timeUse = time_use #np.array(time_use).astype(np.int)
        temp_data_use = temp_data_max #np.array(temp_data_max).astype(np.float)
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(timeUse, temp_data_use)
        
        temp_trend = []
        for i in range(0,len(temp_data_use)):
            temp_in = 0
            temp_in = intercept + slope*timeUse[i]  
            temp_trend.append(temp_in)
        
        temp_result = {"time": [int(str(t)[:4]) for t in time], "data": {"raw":temp_data_max, "trend":temp_trend}, "lat":lat_list[lat_index] , "lon":lon_list[lon_index]}
        return render(request,'graphTrendLinear.html',{"data":temp_result})  

class Graph_avg_10(View):
    def get(self, request):
        name_nc = 'ghcndex_current/GHCND_TXx_1951-2018_RegularGrid_global_2.5x2.5deg_LSmask.nc'
        dataset = Dataset(name_nc, 'r')
        time = dataset.variables["time"][:]
        data = dataset.variables['Ann'][:]

        
        temp_result = {"time": [int(t) for t in time], "data": data}

        lat_index = 58
        lon_index = 13

        i = 10
        temp = []

        while(i < len(time)):
            print(data[i][lat_index][lon_index])
            # temp.append()
            i+=1
        # print(temp_result)
        # print(len(temp_result["time"]),len(temp_result["data"]))

        return render(request,'graphSmooth.html',{"data":"temp_result"})  


class Graph_annual_cycle(View):
    def get(self, request):
        name_nc = 'ghcndex_current/GHCND_TXx_1951-2018_RegularGrid_global_2.5x2.5deg_LSmask.nc'
        dataset = Dataset(name_nc, 'r')
        print(dataset.variables.keys())
        # Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
        time = dataset.variables["time"][:]
        Ann = dataset.variables['Ann'][:]
        Jan = dataset.variables['Jan'][:]
        Feb = dataset.variables['Feb'][:]
        Mar = dataset.variables['Mar'][:]
        Apr = dataset.variables['Apr'][:]
        May = dataset.variables['May'][:]
        Jun = dataset.variables['Jun'][:]
        Jul = dataset.variables['Jul'][:]
        Aug = dataset.variables['Aug'][:]
        Sep = dataset.variables['Sep'][:]
        Oct = dataset.variables['Oct'][:]
        Nov = dataset.variables['Nov'][:]
        Dec = dataset.variables['Dec'][:]

        lat_index = 58
        lon_index = 13

        temp_1 = []
        temp_2 = []
        temp_3 = []
        temp_4 = []
        temp_5 = []
        temp_6 = []
        temp_7 = []
        temp_8 = []
        temp_9 = []
        temp_10 = []
        temp_11 = []
        temp_12 = []

        print(Jan[0][lat_index][lon_index])
    
        for i in range(0,len(time)):
            if(i == len(time)-1):
                break
            temp_1.append(Jan[i][lat_index][lon_index])
            temp_2.append(Feb[i][lat_index][lon_index])
            temp_3.append(Mar[i][lat_index][lon_index])
            temp_4.append(Apr[i][lat_index][lon_index])
            temp_5.append(May[i][lat_index][lon_index])
            temp_6.append(Jun[i][lat_index][lon_index])
            temp_7.append(Jul[i][lat_index][lon_index])
            temp_8.append(Aug[i][lat_index][lon_index])
            temp_9.append(Sep[i][lat_index][lon_index])
            temp_10.append(Oct[i][lat_index][lon_index])
            temp_11.append(Nov[i][lat_index][lon_index])
            temp_12.append(Dec[i][lat_index][lon_index])

        # print(result_fiss)
        result_fish = [np.average(np.array(temp_1)), np.average(np.array(temp_2)), np.average(np.array(temp_3)), np.average(np.array(temp_4)),
                       np.average(np.array(temp_5)), np.average(np.array(temp_6)), np.average(np.array(temp_7)), np.average(np.array(temp_8)),
                       np.average(np.array(temp_9)), np.average(np.array(temp_10)), np.average(np.array(temp_11)), np.average(np.array(temp_12))
                    ]

        print(result_fish)
        lat_list = dataset.variables['lat'][:]
        lon_list = dataset.variables['lon'][:]
        
        timeuse = [str(time[0])[:4], str(time[-2])[:4]]
        print(timeuse)

        temp_result = {"year": {"min":str(time[0])[:4],"max":str(time[-2])[:4]}, "data": result_fish, "lat": lat_list[lat_index], "lon": lat_list[lon_index]}
        # print(temp_result["time"])
        # print(len(temp_result["time"]),len(temp_result["data"]))
        return render(request,'graph_annual_cycle.html',{"data":temp_result})  


# Show all Graph




class AllGraph(View):
    def get(self, request):
        return render(request, 'allGraph.html')

class ShowLocationGraph(View):
    def get(self, request):
        return render(request, 'graphShowOnWeb.html')

class PlotTXx(View):
    def get(self, request):
        
        return render(request,'graphTXx.html')
