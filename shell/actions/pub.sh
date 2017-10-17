curl -i -X POST "https://smartcity.rbccps.org/api/0.1.0/publish" -H 'apikey: b1a7f9f3084b44bea5047a25e782f21a' -d '{"exchange": "amq.topic", "key": "iiot_pub", "body": "$1"}'
