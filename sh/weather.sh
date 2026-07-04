#!/bin/sh
clear
URL='http://www.accuweather.com/ru/ru/saint-petersburg/295212/weather-forecast/295212'
wget -q -O- "$URL" | awk -F\' '/acm_RecentLocationsCarousel\.push/ {x=split($0,Arx,"\"") ; print Arx[2]": "$12"°, "Arx[4]}' | head -1