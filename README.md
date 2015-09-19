# Allb.us

[![Build Status](https://travis-ci.org/CodeforHawaii/allb.us.svg)](https://travis-ci.org/CodeforHawaii/allb.us)

A tiny bus app that's finally being open sourced. Come check us out @ http://allb.us

**Note:** We're currently allbus'. (Here be dragons, local style)

## Installation

### Vagrant

* `vagrant up`
* `vagrant ssh`
* `export DATABASE_URL="postgis://allbus:allbus@localhost:5432/allbus_db"`
* `export DJANGO_SETTINGS_MODULE=config.settings.vagrant`
* `source /var/www/applications/allbus_production/venvs/current/bin/activate`
* `cd /var/www/applications/allbus_production/app/current/etc/`
* `./download_and_install_gtfs_data.sh`
* Open your browser to http://localhost:50808/explore/feed

# License

BSD
