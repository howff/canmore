#!/usr/bin/env python
# 2.00 arb Fru Sep 17 16:00:00 BST 2021 - rewritten in Python
# 1.01 arb Mon Feb  9 12:45:06 GMT 2015
# usage: locationname lat lon radius
# writes to locationname_os-poi.gpx
# Could easily be modified to write KML instead of GPX

from pygeodesy import osgr
import csv
import sys

region_name = sys.argv[1]        # eg. 'Dundee'
center_lat = float(sys.argv[2])  # eg. 56.45
center_lon = float(sys.argv[3])  # eg. -2.97
radius_km  = float(sys.argv[4])  # eg. 60
verbose = 1
poi_csv_file = 'poi_extract_2021-06.csv'

gpx_file = region_name + '_os-poi.gpx'
gridref = osgr.toOsgr(center_lat, center_lon)
center_easting  = gridref.easting  # eg. 340385.0 # Dundee
center_northing = gridref.northing # eg. 730678.0
radius = radius_km * 1000.0        # in m around the center point

num_records = 0
num_ignored = 0
num_class = 0
max_dist_squared = radius * radius

codes_wanted = [
    '03170240', # archaeological
    '03170241', # battlefields
    '03170245', # historical structures
    '03170244', # historical buildings
    '03170246', # historical ships
    '03190257', # scenic features
]


# ---------------------------------------------------
# Example input:
# "UNIQUE_REFERENCE_NUMBER"|"NAME"|"POINTX_CLASSIFICATION_CODE"|"FEATURE_EASTING"|"FEATURE_NORTHING"|"POSITIONAL_ACCURACY_CODE"|"UPRN"|"TOPOGRAPHIC_TOID"|"TOPOGRAPHIC_TOID_VERSION"|"ITN_EASTING"|"ITN_NORTHING"|"ITN_TOID"|"ITN_TOID_VERSION"|"DISTANCE"|"ADDRESS_DETAIL"|"STREET_NAME"|"LOCALITY"|"GEOGRAPHIC_COUNTY"|"POSTCODE"|"VERIFIED_ADDRESS"|"ADMINISTRATIVE_BOUNDARY"|"TELEPHONE_NUMBER"|"URL"|"BRAND"|"QUALIFIER_TYPE"|"QUALIFIER_DATA"|"PROVENANCE"|"DATE_OF_SUPPLY"
# 14356776|"Bowsden West"|"03190259"|398517.8|642006.8|1||"1000000179049100"|6|398745.6|641981.1|"4000000006381055"|2|229.2|""|""|""|"Northumberland"|"TD15"|"N"|"Northumberland"|""|""|""|""|""|"Ordnance Survey"|"2014-12-01"

# Example output:
# <?xml version="1.0" encoding="UTF-8"?>
# <kml xmlns="http://www.opengis.net/kml/2.2">
#  <Document>
#   <Placemark>
#    <name>New York City</name>
#    <description>New York City</description>
#    <Point><coordinates>-74.006393,40.714172,0</coordinates></Point>
#   </Placemark>
#  </Document>
# </kml>

# ---------------------------------------------------
# Convert POINTX_CLASSIFICATION_CODE to a description
# dun_poi_extract/LOOKUP/POI_CLASS_TO_SIC_LOOKUP.txt
# Documentation:
# http://www.ordnancesurvey.co.uk/docs/user-guides/points-of-interest-user-guide.pdf
# Example input:
# 03190259|Trigonometric Points|7420|||||||7112||||||
# codes as GGCCAAAA (GG=group CC=category AAAA=classification)
# Groups:
#   01=accommodation, eating, drinking
#   02 = commercial services
#   03 = attractions
#   04 = sport, entertainment
#   05 = education, health
#   06 = public infrastructure
#   07 = manufacturing, production
#   08 = retail
#   09 = transport
# GroupCategory of interest:
# 0101=accommodation
# 0203=eating,drinking
# 0212=recycling
# 0213=repair and servicing
# 0317=historical and cultural
# 0319=landscape features
# 0423=outdoor pursuits
# 0949=motoring retail
# 1053=air transport
# 1054=road and rail transport
# 1055=walking transport
# 1056=water transport
# 1057=public transport, stations, etc
# 1059=bus transport

poi_desc = {}
with open('POI_CLASS_TO_SIC_LOOKUP.txt') as fd:
    reader = csv.DictReader(fd, delimiter='|')
    for row in reader:
        poi_desc[row['PointX Classification Code']] = row['Description']
        num_class += 1

#print "Read $num_class classifications\n" if ($verbose);

# ---------------------------------------------------------------------
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

def gpx_mark(ofd, name, desc, lat, lon, elev):
    print('<wpt lat="%s" lon="%s">' % (lat, lon), file=ofd)
    print(' <name><![CDATA[%s [%s]]]></name>' % (name, desc), file=ofd)
    print(' <sym>Flag</sym>', file=ofd)
    print(' <type>Marks:OS-POI:%s</type>' % region_name, file=ofd)
    print('</wpt>', file=ofd)

def gpx_footer(fd):
    print('</xml>', file=fd)

# ---------------------------------------------------------------------
def easting_northing_to_latlon(easting, northing):
    e_n = "%f,%f" % (easting, northing)
    ll = osgr.parseOSGR(e_n).toLatLon()
    return (ll[0], ll[1])

# ---------------------------------------------------------------------
def kml_header():
    print("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
    print("<kml xmlns=\"http://www.opengis.net/kml/2.2\">")
    print("<Document>")

def kml_mark(ofd, name, desc, lat, lon, elev):
    print("<Placemark>", file=ofd)
    print("<name>![CDATA[%s]]></name>" % name, file=ofd)
    print("<description>![CDATA[%s]]></description>" % desc, file=ofd)
    print("<Point><coordinates>%f,%f,%f</coordinates></Point>" % (lon,lat,elev), file=ofd)
    print("</Placemark>", file=ofd)

def kml_footer():
    print("</Document>")
    print("</kml>")

# ---------------------------------------------------------------------

# ref_no|name|pointx_class|feature_easting|feature_northing|pos_accuracy|uprn|topo_toid|topo_toid_version|usrn|usrn_mi|distance|address_detail|street_name|locality|geographic_county|postcode|admin_boundary|telephone_number|url|brand|qualifier_type|qualifier_data|provenance|supply_date

print('Writing %s' % gpx_file)
ofd = open(gpx_file, 'w')

gpx_header(ofd)

with open(poi_csv_file) as fd:
    reader = csv.DictReader(fd, delimiter='|')
    for row in reader:
        classif = row['pointx_class']
        if classif not in codes_wanted:
            num_ignored += 1
            continue
        desc = poi_desc[classif]
        name = row['name']
        easting = float(row['feature_easting'])
        northing = float(row['feature_northing'])
        east_diff = abs(easting - center_easting)
        north_diff = abs(northing - center_northing)
        if ((east_diff * east_diff) + (north_diff * north_diff) > max_dist_squared):
            num_ignored += 1
            continue
        (lat,lon) = easting_northing_to_latlon(easting, northing)
        elev = 0

        #kml_mark(ofd, name, desc, lat, lon, elev)
        gpx_mark(ofd, name, desc, lat, lon, elev)

        num_records += 1

gpx_footer(ofd)

