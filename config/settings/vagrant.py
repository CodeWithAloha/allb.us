#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .common import Common
import environ

env = environ.Env()


class Vagrant(Common):

    GEOS_LIBRARY_PATH = env("DJANGO_GEOS_LIBRARY_PATH",
                            default='/usr/lib/x86_64-linux-gnu/libgeos_c.so.1')
    GDAL_LIBRARY_PATH = env("DJANGO_GDAL_LIBRARY_PATH",
                            default='/usr/lib/libgdal.so.1')
    POSTGIS_VERSION = env("DJANGO_POSTGIS_VERSION",
                          default=(2, 2, 2))

    CORS_ORIGIN_ALLOW_ALL = True
# vim: filetype=python
