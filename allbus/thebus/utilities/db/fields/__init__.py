#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db.models import DateTimeField
import datetime


class CreatedDateTimeField(DateTimeField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', False)
        kwargs.setdefault('blank', True)
        kwargs.setdefault('default', datetime.datetime.utcnow)
        super(CreatedDateTimeField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "DateTimeField"


class ModifiedDateTimeField(CreatedDateTimeField):

    def pre_save(self, model, add):
        val = datetime.datetime.utcnow()
        setattr(model, self.attname, val)
        return val

    def get_internal_type(self):
        return "DateTimeField"

# vim: filetype=python
