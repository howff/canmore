#!/usr/bin/env python3

from OSGridConverter import grid2latlong
import csv
import sys

def hdr(fd):
    print("""<?xml version="1.0" encoding="UTF-8" ?>
<gpx version="1.1"
creator="Memory-Map 6.3.3.1261 https://memory-map.com"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xmlns="http://www.topografix.com/GPX/1/1"
 xmlns:xstyle="http://www.topografix.com/GPX/gpx_style/0/2"
 xmlns:xgarmin="http://www.garmin.com/xmlschemas/GpxExtensions/v3"
 xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd http://www.topografix.com/GPX/gpx_style/0/2 http://www.topografix.com/GPX/gpx_style/0/2/gpx_style.xsd http://www.garmin.com/xmlschemas/GpxExtensions/v3 https://www8.garmin.com/xmlschemas/GpxExtensionsv3.xsd">""", file=fd)

with open('megalithic.csv') as fd:
    rdr = csv.reader(fd, delimiter='|')
    rownum = 0
    for row in rdr:
        rownum += 1
        if rownum == 1:
            hdr(sys.stdout)
            continue
        ll = grid2latlong(row[1])
        print('<wpt lat="%s" lon="%s">' % (ll.latitude, ll.longitude))
        print(' <name><![CDATA[%s]]></name>' % row[0])
        print(' <sym>Flag</sym>')
        print(' <type>Marks:Megalithic:Harris</type>')
        print('</wpt>')
print('</gpx>')
