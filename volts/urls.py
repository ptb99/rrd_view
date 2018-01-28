# volts/urls.py - routing file for RRD views

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    url(r'^about/$', views.AboutPageView.as_view(), name='about'),
    url(r'^graph/(?P<dur>[^/]+)', views.GraphView.as_view(), name='graph'),
]
