import requests

header={"content-type":"application/json"}
payloadquery={"timestamp":{"$gt": "Fri, 10 Oct 2014 03:00:00 GMT"}}
payload={"where":payloadquery}


