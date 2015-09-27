#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import gtfs_bus_views
from .views import gtfs_stop_views
from .views import gtfs_trip_views

urlpatterns = [
    # stop views
    url(r'^stops/$', gtfs_stop_views.stop_search, name="stop_search"),

    url(r'^(?P<stop_id>\d+)/$', gtfs_stop_views.stop_details, {'route': None},
        name="stop_details_no_route"),

    url(r'^(?P<stop_id>\d+):(?P<route>[a-zA-Z0-9]+)/$', gtfs_stop_views.stop_details,
        name="stop_details"),

    url(r'^es/near/(?P<latitude>[\-\.0-9]+)/(?P<longitude>[\-\.0-9]+)/$',
        gtfs_stop_views.stop_nearby, name="stop_nearby"),

    # bus views
    url(r'^buses/(?P<bus>[\d]+)$', gtfs_bus_views.bus_details, name="bus_details"),

    # trip views
    url(r'^trips/(?P<trip_id>[\d\.]+)$', gtfs_trip_views.trip_details, name="trip_details"),
]

# vim: filetype=python
