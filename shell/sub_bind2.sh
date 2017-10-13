curl -i -X POST "https://smartcity.rbccps.org/api/0.1.0/subscribe/bind" -H 'apikey: 436d781dfc3a4917914c147bd5f1112a' -d '{"exchange": "amq.topic", "keys": ["iiot_test0"], "queue": "iiot_test0"}'
