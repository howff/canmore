#!/usr/bin/env python3

import csv
import urllib.request
import pandas as pd
from pygeodesy import osgr
import os
import re
import sys

location_name = sys.argv[1]
lat = sys.argv[2]
lon = sys.argv[3]
radius = float(sys.argv[4]) # km
radius_m = int(radius * 1000)

csv_file = location_name + '_canmore.csv'
gridref = osgr.toOsgr(lat, lon)


wanted_groups = [
        'Battle Site',
        'Blackhouse',
        'Broch',
        'Burial Cairn',
        'Burial Ground',
        'Cairn',
        'Castle',
        'Cave',
        'Cemetery',
        'Chain',
        'Chambered Cairn',
        'Chapel',
        'Church',
        'Cinerary Urn',
        'Cist',
        'Clearance Cairn',
        'Cleit',
        'Commemorative Monument',
        'Crannog',
        'Cross Incised Stone',
        'Cross Slab',
        'Cup Marked Rock',
        'Cup Marked Stone',
        'Ditch Defined Cursus',
        'Dovecot',
        'Dun',
        'Fort',
        'Geological Cropmark',
        'Henge',
        'Holy Well',
        'Hut Circle',
        'Icehouse',
        'Inscribed Stone',
        'Kiln',
        'Lade',
        'Long Cairn',
        'Long Cist',
        'Marker Cairn',
        'Mausoleum',
        'Motte',
        'Mound',
        'Natural Feature',
        'Pictish Symbol Stone',
        'Promontory Fort',
        'Recumbent Stone Circle',
        'Reliquary',
        'Rig And Furrow',
        'Ring Cairn',
        'Ring Ditch',
        'Rock Shelter',
        'Sheela Na Gig',
        'Shieling Hut',
        'Souterrain',
        'Standing Stone',
        'Stone',
        'Stone Ball',
        'Stone Circle',
        'Township',
        'Well',
]

# ---------------------------------------------------------------------

def easting_northing_to_latlon(easting, northing):
        e_n = "%f,%f" % (easting, northing)
        ll = osgr.parseOSGR(e_n).toLatLon()
        return (ll[0], ll[1])


# ---------------------------------------------------------------------
# Read the conversion from site type into a code number

csv_sitetypes = pd.read_csv('canmore_sitetypes.csv', index_col=False)
sitetypelist = []
# Get a list of site types we are interested in
# but canmore crashes if list is >100 chars so don't bother unless only a few and a big radius
for wg in wanted_groups:
    code = int(csv_sitetypes[csv_sitetypes['sitetypedesc'] == wg]['sitetypenum'])
    sitetypelist.append(str(code))

# ---------------------------------------------------------------------


print('Writing to %s' % csv_file)
ofd = open(csv_file, 'w')

csv_header = ''

def canmore_append_to_csv(ofd, sitetype=None):
    global csv_header
    canmore_url = "https://canmore.org.uk/canmore_report/site/csv?SITECOUNTRY=1&LOCAT_XY_RADIUS_M=%d&LOCAT_X_COORD=%06d&LOCAT_Y_COORD=%06d&LOCAT_EXTENTTYPE=RADIUS&per_page=1000" % (radius_m, int(gridref.easting), int(gridref.northing))
    if sitetype:
        canmore_url += '&SITETYPE=%s' % sitetype

    print('Requesting %s' % canmore_url)
    with urllib.request.urlopen(canmore_url) as canmore_resp:
        canmore_header = None
        for line in canmore_resp.read().decode().splitlines():
            if re.match('^CANMORE ID.*', line):
                line = line.replace(' ','').lower() + ',lat,lon'
                canmore_header = line
                if not csv_header:
                    csv_header = line
                    print(csv_header, file=ofd)
                continue
            if canmore_header:
                csv_reader = csv.reader( [ line ] )
                csv_fields = next(csv_reader)
                c_easting = float(csv_fields[4])
                c_northing = float(csv_fields[5])
                (c_lat,c_lon) = easting_northing_to_latlon(c_easting, c_northing)
                line = line + '%f,%f' % (c_lat,c_lon)
                print(line, file=ofd)


if len(sitetypelist) > 0:
    for sitetype in sitetypelist:
        canmore_append_to_csv(ofd, sitetype=sitetype)
else:
    canmore_append_to_csv(ofd, sitetype=None)

exit(0)
