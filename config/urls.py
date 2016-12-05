# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.defaults import bad_request
from django.views.defaults import page_not_found
from django.views.defaults import permission_denied
from django.views.defaults import server_error
from django.views.generic import TemplateView


urlpatterns = [
    # Allbus urls
    url(r'^', include("allbus.thebus.urls")),

    # Django Admin
    url(r'^admin/', include(admin.site.urls)),

    # GTFS Explorer
    url(r'^explore$', TemplateView.as_view(template_name="explore/home.html"),
        name='home'),
    url(r'^explore/', include('allbus.exploreapp.urls'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls))
    ]

    urlpatterns += [
        url(r'^400/$', bad_request),
        url(r'^403/$', permission_denied),
        url(r'^404/$', page_not_found),
        url(r'^500/$', server_error)
    ]
