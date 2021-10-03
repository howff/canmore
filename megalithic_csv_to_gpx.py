#!/usr/bin/env python3
# Usage: location_name file.csv
# writes output to file.gpx
# The location_name is used by MemoryMap to put the marks into a folder
#  Marks:Megalithic:location_name

#from OSGridConverter import grid2latlong # Doesn't return correct lat,lon
from pygeodesy import osgr
import csv
import sys

location_name = sys.argv[1]
csv_file = sys.argv[2]
gpx_file = csv_file.replace('.csv','').replace('.CSV','')+'.gpx'

region_name = location_name

def gpx_header(fd):
    print("""<?xml version="1.0" encoding="UTF-8" ?>
<gpx version="1.1"
creator="Memory-Map 6.3.3.1261 https://memory-map.com"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xmlns="http://www.topografix.com/GPX/1/1"
 xmlns:xstyle="http://www.topografix.com/GPX/gpx_style/0/2"
 xmlns:xgarmin="http://www.garmin.com/xmlschemas/GpxExtensions/v3"
 xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd http://www.topografix.com/GPX/gpx_style/0/2 http://www.topografix.com/GPX/gpx_style/0/2/gpx_style.xsd http://www.garmin.com/xmlschemas/GpxExtensions/v3 https://www8.garmin.com/xmlschemas/GpxExtensionsv3.xsd">""",
    file=fd)

def gpx_footer(fd):
    print('</gpx>', file=fd)


print('Writing %s' % gpx_file)
ofd = open(gpx_file, 'w')

gpx_header(ofd)

with open(csv_file) as fd:
    # ngr|lat|lon|site
    rdr = csv.reader(fd, delimiter='|')
    rownum = 0
    for row in rdr:
        rownum += 1
        if rownum == 1:
            continue
        #ll = osgr.parseOSGR(row[0]).toLatLon() # file now has lat,lon so no need for this
        #print('<wpt lat="%s" lon="%s">' % (ll[0], ll[1]), file=ofd)
        print('<wpt lat="%s" lon="%s">' % (row[1], row[2]), file=ofd)
        print(' <name><![CDATA[%s]]></name>' % row[3], file=ofd)
        print(' <sym>Flag</sym>', file=ofd)
        print(' <type>Marks:Megalithic:%s</type>' % region_name, file=ofd)
        print('</wpt>', file=ofd)

gpx_footer(ofd)
