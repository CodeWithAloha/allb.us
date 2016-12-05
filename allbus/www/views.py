#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render


def slash(request):
    return render(request, 'www/slash.html')

# vim: filetype=python
