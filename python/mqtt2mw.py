from smartcity import smartcity as scity
import paho.mqtt.subscribe as subscriber 
import json


SMARTCITY_DEVICE_ID="test_SCMWC0"

print "Available device list..."
print scity.list_devices()


scity_client=scity.Device(SMARTCITY_DEVICE_ID);





while True:
	msg=subscriber.simple("mwdata",qos=1,client_id="mwclient",clean_session=0)
	mqttpayload=msg.payload
	mqttpayload=json.loads(mqttpayload)
	mwpayload=mqttpayload['payload']
	enddevice=data['enddevice']
	





