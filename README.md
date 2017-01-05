# Allb.us

[![Build Status](https://travis-ci.org/CodeforHawaii/allb.us.svg)](https://travis-ci.org/CodeforHawaii/allb.us)

A tiny bus app that's finally being open sourced. Come check us out @ http://allb.us

**Note:** We're currently allbus'. (Here be dragons, local style)

## Installation

You'll need to make sure Python (2.7.X) and Ansible 2.0+ is installed on your machine to run the
Vagrant provisioner.

* `pip install ansible==2.0.2.0`

### Vagrant

#### API KEY

You need to register for an [API KEY](http://hea.thebus.org/api_info.asp). 

Without it, nothing will work. :)


#### Initial load of GTFS data

* `ALLBUS_DIR=<path_to_allbus_location> THEBUS_API_CLIENT_TOKEN=<api_key_from_previous_step> vagrant up`
* `vagrant ssh`
* `sudo -u allbus /bin/bash`
* `source /var/www/applications/allbus_production/venvs/current/bin/activate && pip install django==1.9.12
* `export DJANGO_SETTINGS_MODULE=config.settings`
* `export DJANGO_CONFIGURATION=Vagrant`
* `cd /var/www/applications/allbus_production/app/current/etc/`
* `./download_and_install_gtfs_data.sh`
* `pip install django==1.10.4`

#### Viewing GTFS data

* Open your browser to http://localhost:50808/explore/feed

#### Loading Vue app (only to test out)

*On your local machine (not in vagrant) - at some point, will move to Vagrant

* cd allbus-frontend
* npm run dev
* Open your browser to http://localhost:8080
* Profit!

# TODO

Here are things that still need to be done:

* Need to hook in a modern front end
* Need to internationalize it
* Need to hook in a websocket implementation to bring in gtfs real-time feed

# License

BSD
