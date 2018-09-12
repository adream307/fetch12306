#!/bin/bash
COOKIE_FILE=$PWD/firefox-cookies.txt
CONTENT=test
POST_DATA="act=post&mid=3868401644647971&uid=2946645580&forward=0&isroot=0&content=$CONTENT&location=page_100505_home&module=scommlist&group_source=&pdetail=1005051903401211&_t=0"
USER_AGENT="Mozilla/5.0 (X11; Linux i686; rv:38.0) Gecko/20100101 Firefox/38.0"
RND=`date +%s%3N`

wget -S -d  --user-agent="$USER_AGENT"  --keep-session-cookies \
	--header="Referer: http://weibo.com/u/1903401211" \
	--header="DNT: 1" \
	--header="Pragma: no-cache" \
	--header="X-Requested-With: XMLHttpRequest" \
	 --load-cookies=$COOKIE_FILE \
	 --post-data="$POST_DATA" \
	"http://weibo.com/aj/v6/comment/add?ajwvr=6&__rnd=$RND" \
	-O -
