#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db import models
from .managers import StopManager
from .managers import RouteManager
from .utilities.db.fields import CreatedDateTimeField
from .utilities.db.fields import ModifiedDateTimeField


class AuditableModel(models.Model):

    created_at = CreatedDateTimeField(_('created'))
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="%(app_label)s_%(class)s_creator",
        null=True, blank=True, editable=False)
    modified_at = ModifiedDateTimeField(_('modified'))
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="%(app_label)s_%(class)s_modifier",
        null=True, blank=True, editable=False)

    class Meta:
        abstract = True
        get_latest_by = 'modified_at'
        ordering = ('-modified_at', '-created_at',)


class Route(AuditableModel):

    id = models.BigIntegerField(editable=False, primary_key=True)
    name = models.CharField(max_length=128, null=False, blank=False)
    short_name = models.CharField(max_length=128, null=False, blank=False)

    objects = RouteManager()

    def __unicode__(self):
        return u"%s" % (self.short_name)


class Service(AuditableModel):

    id = models.BigIntegerField(editable=False, primary_key=True)
    start_date = models.DateField()
    end_date = models.DateField()
    MON = models.BooleanField()
    TUE = models.BooleanField()
    WED = models.BooleanField()
    THU = models.BooleanField()
    FRI = models.BooleanField()
    SAT = models.BooleanField()
    SUN = models.BooleanField()

    def __unicode__(self):
        return u"%s" % (self.id)


class Shape(AuditableModel):

    shape_id = models.CharField(max_length=32)
    latitude = models.FloatField(null=False, blank=False)
    longitude = models.FloatField(null=False, blank=False)
    sequence = models.PositiveSmallIntegerField()


class Trip(AuditableModel):

    id = models.BigIntegerField(editable=False, primary_key=True)
    route = models.ForeignKey(Route)
    block_id = models.CharField(max_length=32)
    direction = models.SmallIntegerField()
    headsign = models.CharField(max_length=64)
    service = models.ForeignKey(Service)
    shape_id = models.CharField(max_length=64)

    def __unicode__(self):
        return u"%s" % (self.headsign)


class Stop(AuditableModel):

    code = models.PositiveIntegerField(null=False, blank=False)
    name = models.CharField(max_length=128, null=False, blank=False)
    latitude = models.FloatField(null=False, blank=False)
    longitude = models.FloatField(null=False, blank=False)
    url = models.URLField(null=False, blank=False)
    stop_id = models.CharField(max_length=128, null=False, blank=False)
    objects = StopManager()

    def __unicode__(self):
        return u"%s - %s" % (self.code, self.name)

    @models.permalink
    def get_absolute_url(self):
        return ('stop_details_no_route', (), {'stop': str(self.code)})


class StopTime(AuditableModel):

    trip = models.ForeignKey(Trip)
    stop = models.ForeignKey(Stop)
    sequence = models.PositiveSmallIntegerField()

# vim: filetype=python
