# volts/urls.py - routing file for RRD views

from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.HomePageView.as_view(), name='index'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    re_path('graph/(?P<graph_id>[0-9]+)/', views.GraphView.as_view(), name='graph'),
    path('recipe/', views.RecipeView.as_view(), name='recipe'),
]
