#!/usr/bin/env bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

now=$(date +%Y%m%d-%hh%mm%ss)
gtfs_filepath="$TMPDIR/thebus_gtfs_$now.zip"

curl "http://webapps.thebus.org/transitdata/Production/google_transit.zip" --output $gtfs_filepath

echo "Downloaded TheBus transit data: $gtfs_filepath"

$DIR/../manage.py importgtfs --name thebus $gtfs_filepath
