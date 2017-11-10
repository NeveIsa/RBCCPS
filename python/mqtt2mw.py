from smartcity import smartcity as scity
import paho.mqtt.subscribe as subscriber 
import json
import threading



SMARTCITY_DEVICE_ID="test_SCMWC0"

print "Available device list..."
print scity.list_devices()


scity_client_device=scity.Device(SMARTCITY_DEVICE_ID);



def mwclientthreaded(payload):
	scity_client_device.pub(payload)
	print "\nUploaded--->",payload,"\n"



while True:
	msg=subscriber.simple("mwdata",qos=1,client_id="mwclient",clean_session=0)
	mqttpayload=msg.payload
	print "GOT MQTT--->\n",mqttpayload,"\n"
	#mqttpayload=json.loads(mqttpayload)
	#mwpayload=mqttpayload['payload']
	mwpayload=mqttpayload
	if 'enddevice' in mqttpayload:
		enddevice=mqttpayload['enddevice']

	threading.Thread(target=mwclientthreaded,args=(mwpayload,)).start()






