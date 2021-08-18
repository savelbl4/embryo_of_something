#!/bin/bash
clear
for n in 192.168.{0..3}.{0..10};do ping -c1 $n | grep "bytes from" &>/dev/null
	if [ "$?" -eq "0" ]
	then
		echo -n "$n - "
		echo -e "\033[1;32m"UP
		tput sgr0
	else
		echo -n "$n - "
		echo -e "\033[1;31m"DOWN
		tput sgr0
	fi
done
echo 'ZAEBALO!!!'
exit 0
