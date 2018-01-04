import json
import datetime

class datapacket:
  def __init__(self,deviceid,datatype,dataunit,extract=False):
    self.deviceid=deviceid
    self.datatype=datatype
    self.dataunit=dataunit
    self.extract=extract

  def getpacket(self,rawdata):
    try:
      if type(rawdata)==dict or type(rawdata)==list:
        pass
      else:
        rawdata=json.loads(rawdata)
    except:
      print("Invalid JSON...")
    finally:
      if type(rawdata)==dict:
        rawdatas=[rawdata]
      else:
        rawdatas=rawdata

    payloads=[]

    for rawdata in rawdatas:
      payload={}

      if self.extract and 'timestamp' in rawdata:
        payload['timestamp']=rawdata['timestamp']
      else:
        payload['timestamp']=datetime.datetime.utcnow().isoformat()
        print("Inserting timestamp - %s" %payload['timestamp'])

      payload['deviceid']=self.deviceid
      payload['datatype']=self.datatype
      payload['dataunit']=self.dataunit
      payload['data']=rawdata

      payloads.append(payload)
    return payloads

  def getpacket_esbulk(self,rawdata):
  	es_bulk_meta='{"index":{}}'
  	es_bulk_packet=""
  	payloads=self.getpacket(rawdata)
  	for payload in payloads:
  		es_bulk_packet+=es_bulk_meta+"\n"+json.dumps(payload)+"\n"

  	return es_bulk_packet

  def gettimestampnow(self):
    return datetime.datetime.utcnow().isoformat()

if __name__=="__main__":
  d=datapacket("name","type","unit",extract=True)
  print d.getpacket('{"hello":"world"}')
  print "\n",d.getpacket({"hello":"world"})
  print "\n",d.getpacket([{"hello":"world"},{"hello2":"world2"}])

  import json
  print "\nJSON\n",json.dumps(d.getpacket([{"hello":"world"},{"hello2":"world2"}]))

  print "\n",d.gettimestampnow()

  espack= d.getpacket_esbulk([{"hello":"world"},{"hello2":"world2"}])
  import requests
  rr=requests.put(url="http://localhost:9200/helloworld/middlewaredata/_bulk",headers={"content-type":"application/json"},data=espack)
  print rr.text 