#!/usr/bin/env python3

import csv
import urllib.request
from pygeodesy import osgr
import os
import re
import sys

location_name = sys.argv[1]
lat = sys.argv[2]
lon = sys.argv[3]
radius = sys.argv[4] # km

csv_file = location_name + '_canmore.csv'
gridref = osgr.toOsgr(lat, lon)


# ---------------------------------------------------------------------

def easting_northing_to_latlon(easting, northing):
        e_n = "%f,%f" % (easting, northing)
        ll = osgr.parseOSGR(e_n).toLatLon()
        return (ll[0], ll[1])


# ---------------------------------------------------------------------

canmore_url = "https://canmore.org.uk/canmore_report/site/csv?SITECOUNTRY=1&LOCAT_XY_RADIUS_M=%d&LOCAT_X_COORD=%06d&LOCAT_Y_COORD=%06d&LOCAT_EXTENTTYPE=RADIUS&per_page=99999" % (int(radius)*1000, int(gridref.easting), int(gridref.northing))


print('Requesting %s' % canmore_url)
with urllib.request.urlopen(canmore_url) as canmore_resp:
    print('Writing to %s' % csv_file)
    with open(csv_file, 'w') as fd:
        canmore_header = None
        for line in canmore_resp.read().decode().splitlines():
            if re.match('^CANMORE ID.*', line):
                line = line.replace(' ','').lower() + ',lat,lon'
                canmore_header = line
                print(line, file=fd)
                continue
            if canmore_header:
                csv_reader = csv.reader( [ line ] )
                csv_fields = next(csv_reader)
                c_easting = float(csv_fields[4])
                c_northing = float(csv_fields[5])
                (c_lat,c_lon) = easting_northing_to_latlon(c_easting, c_northing)
                line = line + '%f,%f' % (c_lat,c_lon)
                print(line, file=fd)
