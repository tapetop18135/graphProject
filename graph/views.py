from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse

from netCDF4 import Dataset
import datetime
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


class DataPlotTXx(View):
    def get(self, request):
        data_list = fetchData('ghcndex_current/GHCND_TXx_1951-2018_RegularGrid_global_2.5x2.5deg_LSmask.nc',["time","Ann","lat","lon"])
        time = data_list["time"]
        AnnUse = data_list["Ann"]
        lat_list = data_list["lat"]
        lon_list = data_list["lon"]

        temp_data = []
        for i ,t in enumerate(time):
            if math.isnan(AnnUse[i][58][13]):
                pass
            else:
                temp_data.append(float("{0:.2f}".format(AnnUse[i][58][13])))
        temp_result = {"time": [int(t) for t in time], "data": temp_data}

        return render(request,'graphTXx.html',{"data":temp_result})

class DataPlotTNx(View):
    def get(self, request):
        data_list = fetchData('ghcndex_current/GHCND_TNx_1951-2018_RegularGrid_global_2.5x2.5deg_LSmask.nc',["time","Ann","lat","lon"])
        time = data_list["time"]
        AnnUse = data_list["Ann"]
        lat_list = data_list["lat"]
        lon_list = data_list["lon"]

        temp_data = []
        for i ,t in enumerate(time):
            if math.isnan(AnnUse[i][58][13]):
                pass
            else:
                temp_data.append(float("{0:.2f}".format(AnnUse[i][58][13])))
        temp_result = {"time": [int(t) for t in time], "data": temp_data}

        return render(request,'graphTNx.html',{"data":temp_result})

class AllGraph(View):
    def get(self, request):
        return render(request, 'allGraph.html')


class PlotTXx(View):
    def get(self, request):
        
        return render(request,'graphTXx.html')
