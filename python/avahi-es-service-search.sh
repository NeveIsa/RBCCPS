#!/bin/bash
#avahi-browse _http._tcp -rktp --ignore-local | grep ESDB | grep -P "\d+\.\d+\.\d+\.\d+;\d+" -o

ip=$(avahi-browse _http._tcp -rtp | grep ESDB | grep -P "\d+\.\d+\.\d+\.\d+;\d+" -o)


ip=$(echo $ip | grep -P "\d+\.\d+\.\d+\.\d+" -o)

if [ -z "$ip" ]
then
echo "ES service not found!"
cp _mwconf.json.bak _mwconf.json
else
echo "Found ES service."
echo "{\"ip\":\"$ip\"}" | tee _mwconf.json 
fi


