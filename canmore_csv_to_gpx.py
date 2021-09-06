#!/usr/bin/env python3

import geopandas
import pandas as pd
import re

csv_file = 'harris.csv'
gpx_file = 'harris.gpx'
folder_name = 'Harris'
csv_file = 'stkilda.csv'
gpx_file = 'stkilda.gpx'
folder_name = 'St.Kilda'

wanted_groups = [
        'Blackhouse',
        'Broch',
        'Burial Cairn',
        'Cairn',
        'Cave',
        'Chambered Cairn',
        'Cist',
        'Clearance Cairn',
        'Cleit',
        'Crannog',
        'Cross Slab',
        'Cup Marked Rock',
        'Dun',
        'Hut Circle',
        'Long Cist',
        'Promontory Fort',
        'Rock Shelter',
        'Sheela Na Gig',
        'Souterrain',
        'Standing Stone',
        'Township'
]

def printrow(row):
    # CANMOREID,SITENUMBER,SITENAME,SITETYPE,SITEEASTING,SITENORTHING,COUNCIL,COUNTY,PARISH,NGR,URL
    print('CANMOREID %s' % row.CANMOREID)
    print('SITENUMBER %s' % row.SITENUMBER)
    print('SITENAME %s' % row.SITENAME)
    print('SITETYPE %s' % row.SITETYPE)
    print('E %s' % row.SITEEASTING)
    print('N %s' % row.SITENORTHING)
    print('COUNCIL %s' % row.COUNCIL)
    print('COUNTY %s' % row.COUNTY)
    print('PARISH %s' % row.PARISH)
    print('NGR %s' % row.NGR)
    print('URL %s' % row.URL)
    # This doesn't work, if you add a column to a geopandas dataframe
    # it doesn't show up when you use 'colname' in df.
    # It does however show up in df.dtypes so is definitely there?!
    if 'TYPE' in row:
        print('TYPE %s' % row.TYPE)
    else:
        print('TYPE MISSING')

csv_pd = pd.read_csv(csv_file, index_col=False)

print('PANDAS')
for row in csv_pd.itertuples():
    printrow(row)
    break
print('')

#print(csv_pd.head())
#print(csv_pd.describe())
#print(csv_pd['SITEEASTING'])
#print(csv_pd['CANMOREID'][csv_pd.SITENORTHING == 'WESTERN ISLES'])
#for x in csv_pd:
#    print(x)

csv_geo = geopandas.read_file(csv_file)

print('GEOPANDAS')
for row in csv_geo.itertuples():
    # CANMOREID,SITENUMBER,SITENAME,SITETYPE,SITEEASTING,SITENORTHING,COUNCIL,COUNTY,PARISH,NGR,URL
    printrow(row)
    break
print('')

# Create a GeoDataFrame which has the OS grid ref as x,y
gdf = geopandas.GeoDataFrame(csv_pd,
        geometry=geopandas.points_from_xy(csv_pd['SITEEASTING'], csv_pd['SITENORTHING']), crs='EPSG:27700')
#gdf.set_crs(epsg=27700) # need to assign or change in-place?
# Convert to lat,lon
gdf = gdf.to_crs(epsg=4326)

#print(gdf.geometry)

print('ADDED TYPE COLUMN')
#gdf['TYPE'] = gdf['SITETYPE'].str.extract(r'([^,]*),.*', expand=False) # doesn't work properly, very odd
gdf['TYPE'] = gdf['SITETYPE'].str.split(',').str.get(0).str.split('[^A-Za-z0-9]*\(').str.get(0)
print(gdf.dtypes)
for row in gdf.itertuples():
    printrow(row)
    print('TYPE %s' % row.TYPE)
    break
print('')


gdf_grouped = gdf.groupby('TYPE')

num_groups = 0
num_rows = 0
print('count %s' % gdf_grouped.count())
for name,group in gdf_grouped:
    num_groups += 1
    #print('===============================\nGROUP: %s' % name)
    print('GROUP: %s' % name)
    n = 0
    for rowindex,row in group.iterrows():
        n += 1
        #print(row.SITENAME, row.geometry.x, row.geometry.y)
    #print('GROUP HAD %d rows' % n)
    num_rows += n

print('Groups %d' % num_groups)
print('Total rows %d' % num_rows)

fd = open(gpx_file, 'w')

# Header
print("""<?xml version="1.0" encoding="UTF-8" ?>
<gpx version="1.1"
creator="Memory-Map 6.3.3.1261 https://memory-map.com"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xmlns="http://www.topografix.com/GPX/1/1"
 xmlns:xstyle="http://www.topografix.com/GPX/gpx_style/0/2"
 xmlns:xgarmin="http://www.garmin.com/xmlschemas/GpxExtensions/v3"
 xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd http://www.topografix.com/GPX/gpx_style/0/2 http://www.topografix.com/GPX/gpx_style/0/2/gpx_style.xsd http://www.garmin.com/xmlschemas/GpxExtensions/v3 https://www8.garmin.com/xmlschemas/GpxExtensionsv3.xsd">""", file=fd)


# Output in groups
for group_name,group in gdf_grouped:
    if group_name not in wanted_groups:
        continue
    print('Output %s' % (group_name))
    for rowindex,row in group.iterrows():
        print(f'<wpt lat="{row.geometry.y}" lon="{row.geometry.x}">', file=fd)
        print(f'<name><![CDATA[{row.SITENAME} [{row.SITETYPE}]]]></name>', file=fd)
        print('<sym>Flag</sym>', file=fd)
        print(f'<type>Marks:Canmore:{folder_name}:{group_name}</type>', file=fd)
        print('</wpt>', file=fd)

# Footer
print('</gpx>', file=fd)
