#!/bin/bash
curl --insecure https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8395 | grep -oE "@[^@]+" | gawk '{split($0,z,"|");print z[2],z[3]}'
