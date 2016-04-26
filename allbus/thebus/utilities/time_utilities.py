#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import pytz


def naive_to_timestamp(naive_datetime, tz='Pacific/Honolulu'):
    tz_aware_dt = pytz.timezone(tz).localize(naive_datetime, is_dst=None)
    utc_epoch_dt = datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)
    return int((tz_aware_dt - utc_epoch_dt).total_seconds())

# vim: filetype=python
