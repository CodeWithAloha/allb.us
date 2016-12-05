#!/usr/bin/env bash

sudo -u postgres dropdb allbus_db
sudo -u postgres createdb allbus_db -O allbus
sudo -u postgres psql -c "CREATE EXTENSION postgis;" allbus_db
