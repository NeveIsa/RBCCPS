#!/bin/bash
#avahi-browse _http._tcp -rktp --ignore-local | grep ESDB | grep -P "\d+\.\d+\.\d+\.\d+;\d+" -o

ip=$(avahi-browse _http._tcp -rtp | grep ESDB | grep -P "\d+\.\d+\.\d+\.\d+;\d+" -o)



port=$(echo $ip | grep -P "\;\d+" -o | tr -d ";")
ip=$(echo $ip | grep -P "\d+\.\d+\.\d+\.\d+" -o)



if [ -z "$ip" ]
then
echo "ES service not found!"
cp _mwconf.json.bak _mwconf.json
else
echo "Found ES service -> $ip:$port"
echo "{\"ip\":\"$ip\",\"port\":\"$port\"}" | tee _mwconf.json 
fi


