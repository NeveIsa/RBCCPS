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
        payloads=[rawdata]
      else:
        payloads=rawdata

    for payload in payloads:
      if self.extract and 'timestamp' in rawdata:
        payload['timestamp']=rawdata['timestamp']
      else:
        payload['timestamp']=datetime.datetime.utcnow().isoformat()
        print("Inserting timestamp - %s" %payload['timestamp'])

      payload['data']=rawdata
      payload['deviceid']=self.deviceid
      payload['datatype']=self.datatype
      payload['dataunit']=self.dataunit

    return payloads

  def gettimestampnow(self):
    return datetime.datetime.utcnow().isoformat()

if __name__=="__main__":
  d=datapacket("name","type","unit",extract=True)
  print d.getpacket('{"hello":"world"}')
  print "\n",d.getpacket({"hello":"world"})
  print "\n",d.getpacket([{"hello":"world"},{"hello2":"world2"}])
  print "\n",d.gettimestampnow()
