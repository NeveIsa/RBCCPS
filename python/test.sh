curl -XDELETE localhost:9200/test-test
echo "Deleting test Index"
sleep 2
python elasticclient.py

echo "Waiting for ES to index..."
sleep 3
watch -n 1 'curl -sS  localhost:9200/test-test/_search | jq ".hits"| grep total'
