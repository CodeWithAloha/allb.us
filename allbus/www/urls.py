#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import slash

app_name = 'www'
urlpatterns = [
    url(r'^$', slash, name="slash"),
]

# vim: filetype=python
