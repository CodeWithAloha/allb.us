# Allb.us

[![Build Status](https://travis-ci.org/CodeforHawaii/allb.us.svg)](https://travis-ci.org/CodeforHawaii/allb.us)

A tiny bus app that's finally being open sourced. Come check us out @ http://allb.us

**Note:** We're currently allbus'. (Here be dragons, local style)

## Installation

You'll need to make sure Python (2.7.X) and Ansible 2.0+ is installed on your machine to run the
Vagrant provisioner.

* `pip install ansible==2.0.2.0`

### Vagrant

* `ALLBUS_DIR=<path_to_allbus_location> vagrant up`
* `vagrant ssh`
* `export DJANGO_SETTINGS_MODULE=config.settings`
* `export DJANGO_CONFIGURATION=Vagrant`
* `source /var/www/applications/allbus_production/venvs/current/bin/activate`
* `cd /var/www/applications/allbus_production/app/current/etc/`
* `./download_and_install_gtfs_data.sh`
* Open your browser to http://localhost:50808/explore/feed

# TODO

Here are things that still need to be done:

* Need to hook in a modern front end
* Need to internationalize it
* Need to hook in a websocket implementation to bring in gtfs real-time feed

# License

BSD
