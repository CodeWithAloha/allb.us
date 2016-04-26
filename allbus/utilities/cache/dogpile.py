#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from structlog import get_logger

DOG_PILE_TTL = 30

logger = get_logger()


def cache_get(cache, key):
    logger.bind(key=key)
    logger.debug("cache.get:retrieving key")

    stored_val = cache.get(key)

    # key does not exist, immediately return
    if stored_val is None:
        logger.debug("cache.get:key not found")
        return None

    val, expires, being_refreshed = stored_val

    # Prevent dog-pile
    if (time.time() > expires and not being_refreshed):
        logger.debug("cache.get:preventing dog-piling by setting stale data")
        cache_set(cache, key, val, DOG_PILE_TTL, being_refreshed=True)
        return None

    logger.debug("cache.get:key found!")
    return val


def cache_set(cache, key, val, ttl=0, being_refreshed=False):
    logger.debug(
        "cache.set:attempting to set key with ttl in seconds",
        key=key,
        ttl=ttl)

    real_ttl = time.time() + ttl
    stored_val = (val, real_ttl, being_refreshed)
    return cache.set(key, stored_val)

# vim: filetype=python
