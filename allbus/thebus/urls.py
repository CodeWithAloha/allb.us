#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import stop_views
from .views import route_views

from .views import gtfs_bus_views
from .views import gtfs_stop_views

urlpatterns = [
    # route related views
    url(r'^routes/(?P<route>[a-zA-Z0-9]+)/(?P<direction>(west|east))/$',
        route_views.route_map, name="route_map"),

    # stop related views
    url(r'^stops/$', stop_views.stop_search, name="stop_search"),

    url(r'^(?P<stop>\d+)/$', stop_views.stop_details, {'route': None},
        name="stop_details_no_route"),
    url(r'^(?P<stop>\d+)/map/$', stop_views.stop_map, name="stop_maps"),
    url(r'^(?P<stop>\d+):(?P<route>[a-zA-Z0-9]+)/bus/(?P<bus>\d+)/(?P<direction>(west|east))/$', stop_views.stop_bus_map, name="stop_bus_map"),

    url(r'^(?P<stop>\d+):(?P<route>[a-zA-Z0-9]+)/$', stop_views.stop_details,
        name="stop_details"),

    # converted

    # stop related views
    url(r'^new/(?P<stop>\d+)/$', gtfs_stop_views.stop_details, {'route': None},
        name="stop_details_no_route"),

    url(r'^new/(?P<stop>\d+):(?P<route>[a-zA-Z0-9]+)/$', gtfs_stop_views.stop_details,
        name="stop_details"),

    url(r'^new/es/near/(?P<latitude>[\-\.0-9]+)/(?P<longitude>[\-\.0-9]+)/$',
        gtfs_stop_views.stop_nearby, name="stop_nearby"),

    # bus related views
    url(r'^buses/(?P<bus>[\d]+).json$', gtfs_bus_views.bus_details, name="gtfs_bus_details"),
]

# vim: filetype=python
