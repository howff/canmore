#!/usr/bin/env python3
# Usage: location_name file.csv
# writes output to file.gpx
# The location_name is used by MemoryMap to put the marks into a folder
#  Marks:Canmore:location_name

import geopandas
import pandas as pd
import re
import sys

location_name = sys.argv[1]
csv_file = sys.argv[2]
gpx_file = csv_file.replace('.csv','').replace('.CSV','')+'.gpx'

folder_name = location_name

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

def gpx_header(df):
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

# Read the CSV using Pandas
csv_pd = pd.read_csv(csv_file, index_col=False)

# Create a GeoDataFrame which has the OS grid ref as x,y
gdf = geopandas.GeoDataFrame(csv_pd,
    geometry = geopandas.points_from_xy(csv_pd['siteeasting'], csv_pd['sitenorthing']), crs='EPSG:27700')
# Convert to lat,lon
gdf = gdf.to_crs(epsg=4326)

# Add a type column by extracting the useful info from the sitetype column
gdf['type'] = gdf['sitetype'].str.split(',').str.get(0).str.split('[^A-Za-z0-9]*\(').str.get(0)

# Group by the new type
gdf_grouped = gdf.groupby('type')

# Output GPX

fd = open(gpx_file, 'w')

gpx_header(fd)

# Output in groups

for group_name,group in gdf_grouped:
    if group_name not in wanted_groups:
        continue
    for rowindex,row in group.iterrows():
        print(f'<wpt lat="{row.geometry.y}" lon="{row.geometry.x}">', file=fd)
        print(f'<name><![CDATA[{row.sitename} [{row.sitetype}]]]></name>', file=fd)
        print('<sym>Flag</sym>', file=fd)
        print(f'<type>Marks:Canmore:{folder_name}:{group_name}</type>', file=fd)
        print('</wpt>', file=fd)

gpx_footer(fd)

