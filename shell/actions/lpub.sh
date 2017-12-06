curl -ik -X POST "https://localhost:8443/api/0.1.0/publish" -H 'apikey: eb154e8053ea4687a55187c6028ff150' -d '{"exchange": "amq.topic", "key": "123sub", "body": "'$1'"}'
