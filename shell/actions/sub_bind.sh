curl -i -X POST "https://smartcity.rbccps.org/api/0.1.0/subscribe/bind" -H 'apikey: fcfdae8da95049998b453568733e0cd4' -d '{"exchange": "amq.topic", "keys": ["iiot_pub"], "queue": "iiot_sub"}'
