curl -i -X POST "https://smartcity.rbccps.org/api/0.1.0/subscribe/bind" -H 'apikey: b1a10d8341fc4fbc891265cee14d5edc' -d '{"exchange": "amq.topic", "keys": ["iiot_dummy"], "queue": "iiot_dummy"}'
