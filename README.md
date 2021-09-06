# Canmore

## Download CSV file

https://canmore.org.uk/canmore_report/site/csv?SITECOUNTRY=1&LOCAT_XY_RADIUS_M=12000&LOCAT_X_COORD=106400&LOCAT_Y_COORD=891900&LOCAT_EXTENTTYPE=RADIUS&per_page=9999

After downloading CSV you need to remove the canmore preamble to get to the CSV header row.
Then remove spaces from column names in the header.

# Create a Python virtualenv

```
virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
python3 -m pip install pandas geopandas 
```


# Extract a subset as GPX

The groups are simplified by removing everything in brackets.
Extracts a subset of the different groups, based on personal preference.

Edit the script with filenames, and other preferences, then
```
./canmore_csv_to_gpx.py
```

## Note on EPSG codes

British National Grid = BNG = OSGB 36 National Grid = EPSG: 27700

WGS 84 = ETRS89 = EPSG: 4326
