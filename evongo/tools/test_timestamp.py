import requests,json,datetime

payload=json.dumps({'timestamp':datetime.datetime.utcnow().isoformat()})
header={'content-type':'application/json'}
url='http://localhost:5000/middlewaredata'

print requests.post(url,headers=header,data=payload).text
