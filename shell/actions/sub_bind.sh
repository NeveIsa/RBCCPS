curl -i -X POST "https://smartcity.rbccps.org/api/0.1.0/subscribe/bind" -H 'apikey: ecb7b9f10419446ba0b9bfd94a5ec12b' -d '{"exchange": "amq.topic", "keys": ["iiot_pub2"], "queue": "iiot_sub2"}'
