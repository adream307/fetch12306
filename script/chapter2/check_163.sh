#!/bin/bash
n=1;
while [ $n -gt 0 ];
do
	sudo netstat -anp | grep -E "(114.80.143.158)|(101.227.66.158)"
	echo $((n=n+1))
	sleep 1;
done
