from django.urls import path
from . import views
urlpatterns = [
    path('allGraph', views.AllGraph.as_view(), name='showAllGraph'),
    path('graphtxx', views.DataPlotTXx.as_view(), name='TXxGraph'),
    path('graphtnx', views.DataPlotTNx.as_view(), name='TNxGraph'),
    path('avgworldgraphtxx', views.DataPlotWorldTXx.as_view(), name='WorldTXxGraph'),
    path('avgworldgraphtnx', views.DataPlotWorldTNx.as_view(), name='WorldTNxGraph'),
    path('plottxx', views.PlotTXx.as_view(), name='PlotTXx'),

    
    # Location

    path('showLocationGraph', views.ShowLocationGraph.as_view(), name='showAlllocationGraph'),

    # fix year
    path('graph_tem_pre', views.Graph_temp_rain.as_view(), name='RainFall_TempGraph'),

    # time Series
    path('graph_tmin_tmax', views.Graph_temp_max_min.as_view(), name='Tmin_Tmax'),
    path('graph_avg_10', views.Graph_avg_10.as_view(), name='temp_avg10'),
    path('graph_linear_regression', views.Graph_trend_line.as_view(), name='temp_linear_regression'),
    path('annual_cycle', views.Graph_annual_cycle.as_view(), name='temp_annual_cycle'),

]
