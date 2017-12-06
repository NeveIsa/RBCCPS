import requests
import json


## TO PRINT WHAT REQUESTS IS SENDING, PATH+CH httplib send method
import httplib
def patch_send():
    old_send= httplib.HTTPConnection.send
    def new_send( self, data ):
        print data
        return old_send(self, data) #return is not necessary, but never hurts, in case the library is changed
    httplib.HTTPConnection.send= new_send






EVANGO_HOST="http://desktop:8000/evango/middle"


def evangopub(payload):
  headers = {'Content-Type': 'application/json',}
  
  try:
  	json.loads(payload)
  except Exception as e:
  	print "\n--->PAYLOAD is not a valid JSON"
  	return False

  return requests.post('http://desktop:8000/evongo/middlewaredata', headers=headers, data=payload)


if __name__=="__main__":
  import sys
  
  #patch_send()

  test_data='[{"firstname": "barack", "lastname": "obama3333"}, {"firstname": "mitt", "lastname": "romney"}]'
  data= sys.argv[1] if len(sys.argv)>1 else test_data
  print '\n---> publishing... %s' % data
  evangopub(data)
