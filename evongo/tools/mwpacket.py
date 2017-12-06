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
      rawdata=json.loads(rawdata)
    except:
      print("Invalid JSON...")

    if self.extract and 'timestamp' in rawdata:
      payload['timestamp']=rawdata['timestamp']
    else:
      payload['timestamp']=datetime.datetime.utcnow().isoformat()

    payload['data']=rawdata
    payload['deviceid']=self.deviceid
    payload['datatype']=self.datatype
    payload['dataunit']=self.dataunit

    return payload


if __name__=="__main__":
  d=datapacket("name","type","unit")
  print d.getpacket('{"hello":"world"}')
