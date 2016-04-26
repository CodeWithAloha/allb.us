#!/usr/bin/env bash

sudo -u postgres dropdb allbus
sudo -u postgres createdb allbus -O allbus
sudo -u postgres psql -c "CREATE EXTENSION postgis;" allbus
