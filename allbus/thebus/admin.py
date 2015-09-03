#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Route
from .models import Service
from .models import Shape
from .models import Trip
from .models import Stop
from .models import StopTime


class RouteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'short_name', 'modified_at', 'created_at')
    ordering = ('id',)
admin.site.register(Route, RouteAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_date', 'end_date', 'MON', 'TUE', 'WED', 'THU',
                    'FRI', 'SAT', 'SUN', 'modified_at', 'created_at')
    ordering = ('id',)
admin.site.register(Service, ServiceAdmin)


class ShapeAdmin(admin.ModelAdmin):
    list_display = ('id', 'shape_id', 'latitude', 'longitude', 'sequence',
                    'modified_at', 'created_at')
    ordering = ('id', 'shape_id', 'sequence')
admin.site.register(Shape, ShapeAdmin)


class TripStopTimeInline(admin.TabularInline):
    model = StopTime
    fields = ('stop', 'sequence')
    raw_id_fields = ('stop',)
    ordering = ('sequence',)


class TripAdmin(admin.ModelAdmin):
    list_display = ('id', 'headsign', 'route', 'block_id', 'direction',
                    'service', 'shape_id', 'modified_at', 'created_at')
    ordering = ('id',)
    inlines = [TripStopTimeInline]
admin.site.register(Trip, TripAdmin)


class StopAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'latitude', 'longitude', 'url')
    ordering = ('code',)
admin.site.register(Stop, StopAdmin)


class StopTimeAdmin(admin.ModelAdmin):
    list_display = ('trip', 'stop', 'sequence')
    ordering = ('stop', 'sequence',)
admin.site.register(StopTime, StopTimeAdmin)

# vim: filetype=python
