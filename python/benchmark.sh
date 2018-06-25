eshost=$(cat _mwconf.json | jq '.ip' | tr -d '"')
echo $eshost
#exit
curl -XDELETE $eshost:9200/test-test
echo "Deleting test Index"
sleep 2
python elasticclient.py $1

echo "Waiting for ES to index..."
sleep 5
watch -n 1 "curl -sS  $eshost:9200/test-test/_search | jq \".hits\"| grep total"
