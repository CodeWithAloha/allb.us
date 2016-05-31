# -*- coding: utf-8 -*-

from .common import Common
import environ

env = environ.Env()


class Production(Common):
    pass
