#!/bin/bash
curl -iv --raw -H "Accept-Encoding: gzip deflate" \
               -H "User-Agent: Mozilla/5.0 (X11; Linux i686; rv:38.0) Gecko/20100101 Firefox/38.0" \
               -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
               -H "Referer: http://www.163.com" \
                http://www.163.com -o 163.raw
