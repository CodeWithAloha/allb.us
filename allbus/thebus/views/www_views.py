#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response
from ..utilities.cache.decorators import cacheable

from django.core.cache import cache
from django.conf import settings
from django.utils.translation import get_language

import inspect


def django_view_key_fun(fun, *args, **kwargs):
    name = fun.__name__
    mod = fun.__module__
    call_args = inspect.getcallargs(fun, *args, **kwargs)
    request = call_args.get('request', None)

    if request:
        del call_args['request']

    key = "%s-%s-%s" % (
        name, mod, '-'.join(
            ["%s-%s" % (k, call_args[k]) for k in sorted(call_args.iterkeys())]))

    if request and (settings.USE_I18N or settings.USE_L10N):
        key = "%s-%s" % (key, getattr(request, 'LANGUAGE_CODE', get_language()))

    return key


@cacheable(cache=cache, key=django_view_key_fun, ttl=60*60)
def slash(request):
    return render_to_response('www/slash.html', {},
                              context_instance=RequestContext(request))


@cacheable(cache=cache, key=django_view_key_fun, ttl=60*60)
def placard(request):
    return render_to_response('www/placard.html', {},
                              context_instance=RequestContext(request))


@cacheable(cache=cache, key="about", ttl=60*60)
def about(request):
    return render_to_response('www/about.html', {},
                              context_instance=RequestContext(request))

# vim: filetype=python
