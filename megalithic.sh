#!/bin/bash

lat="57.81"
lon="-6.95"

if [ ! -f article.html ]; then
curl "https://www.megalithic.co.uk/article.php?long=${lon}&lat=${lat}" \
  -H 'Connection: keep-alive' \
  -H 'Cache-Control: max-age=0' \
  -H 'sec-ch-ua: "Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'DNT: 1' \
  -H 'Upgrade-Insecure-Requests: 1' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36' \
  -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'Sec-Fetch-Mode: navigate' \
  -H 'Sec-Fetch-User: ?1' \
  -H 'Sec-Fetch-Dest: document' \
  -H 'Referer: https://www.megalithic.co.uk/search.php' \
  -H 'Accept-Language: en-GB,en-US;q=0.9,en;q=0.8' \
  -H 'Cookie: lang=english; PHPSESSID=joqqhkuvv5mdpmjrbbqle2aru2' \
  > article.html
fi

# <a href="article.php?sid=8373&amp;all=1&amp;noglimit=1#nearby">View more nearby sites and additional images</a>

nexturl="https://www.megalithic.co.uk/"`grep 'View more nearby sites and additional images' article.html | sed -e 's/.*href="//' -e 's/".*//'`

if [ ! -f list.html ]; then
curl "$nexturl" \
  -H 'Connection: keep-alive' \
  -H 'sec-ch-ua: "Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'Upgrade-Insecure-Requests: 1' \
  -H 'DNT: 1' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36' \
  -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'Sec-Fetch-Mode: navigate' \
  -H 'Sec-Fetch-User: ?1' \
  -H 'Sec-Fetch-Dest: document' \
  -H 'Referer: https://www.megalithic.co.uk/article.php?long=-2.97&lat=56.46' \
  -H 'Accept-Language: en-GB,en-US;q=0.9,en;q=0.8' \
  -H 'Cookie: lang=english; PHPSESSID=joqqhkuvv5mdpmjrbbqle2aru2' \
  > list.html
fi

echo 'site|ngr' > megalithic.csv
grep 'article.php?sid=.*<i>' list.html | sed -e 's/^.*href="[^"]*">//' \
	-e 's,<i>,,g' -e 's,</i>,,g' -e 's,<br>,,g' -e 's,</a>,,g' -e 's,(\([A-Z][A-Z][0-9][0-9]*\)),|\1,' \
	>> megalithic.csv

