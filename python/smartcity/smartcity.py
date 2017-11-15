import requests
import sys
import json
import os

import pkg_resources



##GLOBALS

GLOBAL_SSL_VERIFY=False
MIDDLEWARE_SERVER_NAME="https://smartcity.rbccps.org"
#MIDDLEWARE_SERVER_NAME="https://10.156.14.144"


if not GLOBAL_SSL_VERIFY:
  requests.packages.urllib3.disable_warnings()

__userFile=pkg_resources.resource_filename(__name__,'_user.json')

__devicesFile=pkg_resources.resource_filename(__name__,'_devices.json')


def resID2apiKey(resID):
  if not os.path.exists(__devicesFile):
    print "Creating new file: %s" % __devicesFile
    with open(__devicesFile,'w') as g:
      g.write("{}")
      pass
  devices=json.loads(open(__devicesFile).read())
  if resID in devices:
    return devices[resID]
  else:
    return None


def getUser4mFile():
  if not os.path.exists(__userFile):
    print "No user exist... Create a new User? [Y/n]"
    ans=raw_input().upper().strip()
    if ans=="Y":
      print "username: ",
      username=raw_input().strip()
      print "apikey: ",
      api_key=raw_input().strip()
      with open(__userFile,'w') as g:
        g.write(json.dumps({'username':username,'apiKey':api_key}))
    else:
     print "---> A user needs to be created before creating a device..."
     raise Exception

  return json.loads(open(__userFile).read())

def newDevice(resource_id,dev_type):
  userDetails=getUser4mFile()
  print "Found user -> ",userDetails
  user=User(userDetails['apiKey'])

  with open(__devicesFile) as f:
    devices=json.loads(f.read())

  if dev_type=="sensor":
    service_type="publish"
  elif dev_type=="actuator":
    service_type="publish,subscribe"
  elif dev_type=="application":
    service_type="publish,subscribe,historicData"
  else:
    print "---> 'dev_type' parameter can only accept values publish,subscribe,historicData"
    raise Exception

  deviceDetails=user.onboard(resource_id,service_type)
  devices[resource_id]=deviceDetails

  with open(__devicesFile,'w') as g:
    g.write(json.dumps(devices))

  return deviceDetails

class User:
  def __init__(self,api_key):
    self.apikey=api_key

  def onboard(self,resource_id,service_type):
    """
    Use: Register a device
    Params: resource_id,service_type(publish,subscribe,historicData)
    """
    headers = {'apikey': self.apikey,'resourceID':resource_id,'serviceType':service_type}
    result=requests.get("%s/api/0.1.0/register"%MIDDLEWARE_SERVER_NAME,headers=headers,verify=GLOBAL_SSL_VERIFY)
    if result.status_code == requests.codes.ok:
      print "--->","Raw reply for registration from server follows..."
      print result.text
      print "<---","Raw reply for registration from server ends..."

      response=json.loads(result.text[:-331]+"}")
      response["Registration"]="success"

      if response['Registration']=="success":
        print "device registered successfully..."
        print response
        return response
      else:
        print "---> Could not register the new device {0}".format(resource_id)
        print "--->",response
        raise Exception
    else:
      print "---> Could not register the new device {0}".format(resource_id)
      print "--->",result.text
      raise Exception


class Device:
  def __init__(self,resource_id,dev_type="application"):

    self.resource_id=resource_id
    self.dev_type=dev_type

    foundDev=resID2apiKey(resource_id)

    if foundDev:
      APIKey=foundDev['APIKey']
      print "---> Device found \n - {0} : {1}".format(resource_id,APIKey)
      self.api_key=APIKey
      #self.dev_type=foundDev['devType']
    else:
      print "Create a new device with resource_id '{0}' of type '{1}' ? [Y,n] ".format(resource_id,dev_type),
      ans=raw_input().upper()
      if ans=="Y":
        deviceDetails=newDevice(resource_id,dev_type)
        self.api_key=deviceDetails["APIKey"]
      else:
        print "---> Device not created... Exiting..."
        raise Exception

    if dev_type=="sensor":
      self.service_type="publish"
    elif dev_type=="actuator":
      self.service_type="publish,subscribe"
    elif dev_type=="application":
      self.service_type="publish,subscribe,historicData"
    else:
      print "---> 'dev_type' parameter can only accept values publish,subscribe,historicData"
      raise Exception

  def bind(self,resource_id_to_bind):
    """Bind before substribing"""
    self.resource_id_to_bind=resource_id_to_bind
    headers={'apikey':self.api_key}
    data={"exchange": "amq.topic", "keys": ["%s" % resource_id_to_bind], "queue": "%s" % self.resource_id}
    result=requests.post("%s/api/0.1.0/subscribe/bind"%MIDDLEWARE_SERVER_NAME,headers=headers,data=json.dumps(data),verify=GLOBAL_SSL_VERIFY)
    if result.status_code == requests.codes.ok:
      print "---> Binding to %s" % resource_id_to_bind
      print " -",result.text
      return True
    else:
      print "---> Could not publish data to %s" % resource_id_to_bind
      print " -",result.status_code
      print " -",result.text
      return False

  def unbind(self):
    """Unbind"""
    pass

  def sub(self):
    """Subscribe"""
    print "---> Subscribing to 'resource_id' - %s" % self.resource_id_to_bind
    headers={'apikey':self.api_key}
    r=requests.get("%s/api/0.1.0/subscribe?name=%s" % (MIDDLEWARE_SERVER_NAME,self.resource_id_to_bind),headers=headers,stream=True,verify=GLOBAL_SSL_VERIFY)
    for line in r.iter_lines():
      print line

  def pub(self,payload,subtopic=None,topic=None):
    """Publish"""

    headers={'apikey':self.api_key}

    publish_topic = self.resource_id

    if subtopic:
      publish_topic+="/"+subtopic

    if topic:
      publish_topic=topic

    data={"exchange": "amq.topic", "key": "%s" % publish_topic, "body": "%s" % payload}
    result=requests.post("%s/api/0.1.0/publish"%MIDDLEWARE_SERVER_NAME,headers=headers,data=json.dumps(data),verify=GLOBAL_SSL_VERIFY)
    if result.status_code == requests.codes.ok:
      print "---> Publishing data :",payload
      print " -",result.text
      return True
    else:
      print "---> Could not publish data"
      print " -",result.status_code
      print " -",result.text
      return False



def list_devices():
  with open(__devicesFile) as f:
    devices=json.loads(f.read())

  for dev in devices:
    print "--->",dev
    print devices[dev],"\n"

  return devices

if __name__=="__main__":

  supported_args=["dryrun","lsdev","pub","sub"]

  import sys
  try:
    arg=sys.argv[1]
    if arg in supported_args:
      pass
    else:
      print "Supported arguments :",supported_args

  except Exception:
    print "Need arguements :",supported_args
    exit()

  if arg=="dryrun":
    temp_res_id=sys.argv[2]
    d=Device(temp_res_id)
    #d.bind("iiot_dummy")
    d.bind(temp_res_id)
    d.pub("hello world")
    d.sub()

  if arg=="pub":
    res_id=sys.argv[2]
    if len(sys.argv)<=4:
      data=sys.argv[3]
    else:
      pub_topic=sys.argv[3]
      data=sys.argv[4]
    d=Device(res_id)
    d.pub(data,topic=pub_topic)

  if arg=="sub":
    res_id_this_device=sys.argv[2]
    res_id_target_device=sys.argv[3]
    d=Device(res_id_this_device)
    d.bind(res_id_target_device)
    d.sub()

  elif arg=="lsdev":
    list_devices()
