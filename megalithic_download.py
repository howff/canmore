#!/usr/bin/env python3
# usage:   name lat lon
# writes to {name}_megalithic.csv

import os
import re
import sys
import urllib.request
from pygeodesy import osgr

location_name = sys.argv[1]
lat = sys.argv[2]
lon = sys.argv[3]

csv_file = location_name + '_megalithic.csv'

mega_encoding = 'cp1252' # assume Windows encoding for this website (it breaks with utf-8)


# ---------------------------------------------------------------------
mega_url = f"https://www.megalithic.co.uk/article.php?long={lon}&lat={lat}"
print('Requesting URL %s' % mega_url)
mega_req = urllib.request.Request(mega_url)
mega_req.add_header('Referer', 'https://www.megalithic.co.uk/search.php')
mega_req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36')
#mega_req.add_header('Cookie', 'lang=english; PHPSESSID=joqqhkuvv5mdpmjrbbqle2aru2')
mega_resp = urllib.request.urlopen(mega_req)
mega_article = mega_resp.read().decode(mega_encoding)
# Look for this in the page:
# <a href="article.php?sid=8373&amp;all=1&amp;noglimit=1#nearby">View more nearby sites and additional images</a>
mega_nearby_match = re.search('"(article.php[^"]*)">View more nearby sites', mega_article)
if not mega_nearby_match:
    print('ERROR: cannot find nearby sites in %s (see tmp file)' % mega_url)
    with open('tmp', 'w') as fd:
        print(mega_article, file=fd)
    exit(1)

# ---------------------------------------------------------------------
mega_nearby_url = "https://www.megalithic.co.uk/" + mega_nearby_match.group(1)
print('Requesting URL %s' % mega_nearby_url)
mega_req = urllib.request.Request(mega_nearby_url)
mega_req.add_header('Referer', mega_url)
mega_req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36')
#mega_req.add_header('Cookie', 'lang=english; PHPSESSID=joqqhkuvv5mdpmjrbbqle2aru2')
mega_resp = urllib.request.urlopen(mega_req)
mega_listing = mega_resp.read().decode(mega_encoding).splitlines()

# ---------------------------------------------------------------------
with open(csv_file, 'w') as fp:
    print('ngr|lat|lon|site', file=fp)
    for line in mega_listing:
        # Look for lines like this:
        # &nbsp;11.1km SE 135&#x00B0; <a href="article.php?sid=3387">Melgum NW</a> Stone Circle (<i>NJ471053</i>)<br>
        m = re.search(r'article.php\?sid=[^"]*">(.*)</a> (.*) \(<i>(.*)</i>\)', line)
        if m:
            latlon = osgr.parseOSGR(m.group(3)).toLatLon()
            print('%s|%f|%f|%s (%s)' % (m.group(3), latlon[0], latlon[1], m.group(1), m.group(2)), file=fp)
