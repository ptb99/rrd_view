# volts/urls.py - routing file for RRD views

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='index'),
    url(r'^about/$', views.AboutPageView.as_view(), name='about'),
    url(r'^graph/(?P<graph_id>[0-9]+)/$', views.GraphView.as_view(), name='graph'),
]
