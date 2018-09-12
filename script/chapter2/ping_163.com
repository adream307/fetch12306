#!/bin/bash
n=0
while [ $n -lt 10 ]
do
	ping www.163.com -c 1 &
	((n=n+1))
done
