import requests

EVANGO_HOST="http://desktop:8000/evango/middle"







def evangopub(payload):
  headers = {'Content-Type': 'application/json',}
  data = [payload]
  requests.post('http://desktop:8000/evongo/middlewaredata', headers=headers, data=data)

