from smartcity import smartcity as scity
import paho.mqtt.subscribe as subscriber 
import json
from multiprocessing.dummy import Pool as ThreadPool



SMARTCITY_DEVICE_ID="test_SCMWC0"

print "SMARTCITY_DEVICE_ID >",SMARTCITY_DEVICE_ID

print "Available device list..."
print scity.list_devices()


scity_client_device=scity.Device(SMARTCITY_DEVICE_ID);



def mwclientthreaded(payload):
	try:
		scity_client_device.pub(payload)
	except:
		pass

	print "\nUploaded--->\n",payload,"\n"



#Initialize a pool of worker threads
pool=ThreadPool(70)



while True:
	try:
		msg=subscriber.simple("mwdata",qos=1,client_id="mwclient",clean_session=0)
	except Exception as e:
		print "Cannot contact MQTT Broker ---> \n",e
		exit(-1)

	mqttpayload=msg.payload
	print "GOT MQTT--->\n",mqttpayload,"\n"
	#mqttpayload=json.loads(mqttpayload)
	#mwpayload=mqttpayload['payload']
	mwpayload=mqttpayload
	if 'enddevice' in mqttpayload:
		enddevice=mqttpayload['enddevice']

	pool.apply_async(mwclientthreaded,(mwpayload,))






