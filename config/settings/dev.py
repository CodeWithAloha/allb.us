# -*- coding: utf-8 -*-

from .common import Common
import environ

env = environ.Env()


class Dev(Common):

    GEOS_LIBRARY_PATH = env("DJANGO_GEOS_LIBRARY_PATH",
                            default='/opt/local/lib/libgeos_c.dylib')
    GDAL_LIBRARY_PATH = env("DJANGO_GDAL_LIBRARY_PATH",
                            default='/opt/local/lib/libgdal.dylib')
    POSTGIS_VERSION = env("DJANGO_POSTGIS_VERSION",
                          default=(2, 2, 1))
