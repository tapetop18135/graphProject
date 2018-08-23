from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse

from netCDF4 import Dataset
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

        return render(request,'graphWorldTXx.html',{"data":temp_result})        

class DataPlotWorldTNx(View):
    def get(self, request):
        name_nc = 'ghcndex_current/GHCND_TNx_1951-2018_RegularGrid_global_2.5x2.5deg_LSmask.nc'
        dataset = Dataset(name_nc, 'r')
        time = dataset.variables["time"][:]
        data = fetAvgWorldData(dataset.variables['Ann'][:])

        temp_result = {"time": [int(t) for t in time], "data": data}

        return render(request,'graphWorldTNx.html',{"data":temp_result})        

    

class AllGraph(View):
    def get(self, request):
        return render(request, 'allGraph.html')




class PlotTXx(View):
    def get(self, request):
        
        return render(request,'graphTXx.html')
