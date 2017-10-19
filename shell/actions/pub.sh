curl -i -X POST "https://smartcity.rbccps.org/api/0.1.0/publish" -H 'apikey: a65b52992128498fb07ff3ee3fb4fc30' -d '{"exchange": "amq.topic", "key": "iiot_pub2", "body": "'$1'"}'
