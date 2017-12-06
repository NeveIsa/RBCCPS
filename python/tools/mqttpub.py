
## SAMPLE CODE TAKEN FROM
## https://www.hivemq.com/blog/mqtt-client-library-paho-python

import paho.mqtt.client as paho
import time
import sys

def on_publish(client, userdata, mid):
    print("mid: "+str(mid))

client = paho.Client()
client.on_publish = on_publish
client.connect("localhost", 1883)
client.loop_start()




def mwpub(data):
	(rc, mid) = client.publish("mwdata", data, qos=1)
	print "---> data : %s " % data
	return (rc,mid)





if __name__=="__main__":
	delay=1
	if len(sys.argv)>1:
		delay=float(sys.argv[1])

	TEMP_COUNT=0
	def read_from_imaginary_thermometer():
		global TEMP_COUNT
		TEMP_COUNT+=1
		return TEMP_COUNT


	while True:
		temperature = read_from_imaginary_thermometer()
		(rc, mid) = mwpub('{"temp":"%s"}' % str(temperature))
		time.sleep(delay)
