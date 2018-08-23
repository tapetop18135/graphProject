from django.urls import path
from . import views
urlpatterns = [
    path('allGraph', views.AllGraph.as_view(), name='showAllGraph'),
    path('graphtxx', views.DataPlotTXx.as_view(), name='TXxGraph'),
    path('graphtnx', views.DataPlotTNx.as_view(), name='TNxGraph'),
    path('avgworldgraphtxx', views.DataPlotWorldTXx.as_view(), name='WorldTXxGraph'),
    path('avgworldgraphtnx', views.DataPlotWorldTNx.as_view(), name='WorldTNxGraph'),
    path('plottxx', views.PlotTXx.as_view(), name='PlotTXx'),
]
