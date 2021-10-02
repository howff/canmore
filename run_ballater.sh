#!/bin/bash

location_name="ballater"
lat="57.207433"
lon="-3.047955"
radius="15"

./canmore_download.py "$location_name" "$lat" "$lon" "$radius"
./canmore_csv_to_gpx.py "$location_name" "${location_name}_canmore.csv"

./megalithic_download.py "$location_name" "$lat" "$lon"
./megalithic_csv_to_gpx.py "$location_name" "${location_name}_megalithic.csv"

./poi_to_gpx.py "$location_name" "$lat" "$lon" "$radius"
