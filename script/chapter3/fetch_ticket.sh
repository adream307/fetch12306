#!/bin/bash
CNT=0
while [ 1 -gt 0 ]; do
	NUM=`curl --insecure --user-agent "Mozilla/5.0 (X11; Linux i686; rv:38.0) Gecko/20100101 Firefox/38.0" "https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate=2016-12-21&from_station=SHH&to_station=VHH" | grep -oP "(?<={)[^{}]+(?=})" | grep "G7521" | sed -r 's/.*ze_num":"([^"]+).*/\1/'`
	echo "fetch G7521"
	if [ $NUM = "无" ]; then
		CNT=$((CNT+1))
	else
		paplay /usr/share/sounds/ubuntu/stereo/phone-incoming-call.ogg
	fi
	echo $CNT
	sleep 10
done

