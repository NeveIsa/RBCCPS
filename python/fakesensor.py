
## SAMPLE CODE TAKEN FROM
## https://www.hivemq.com/blog/mqtt-client-library-paho-python
import datetime
import paho.mqtt.client as paho
import time
import sys
import random
from tools import mwpacket
import json

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
		return int(random.random()*100)
		return TEMP_COUNT



        imu_sensor_data = json.loads(open("imu_sensor.json").read())
	d=mwpacket.datapacket("name","type","unit",extract=True)
        mid=0
	while True:
		temperature = 100 #read_from_imaginary_thermometer()
                pack=['{"timestamp":"%s","deviceid":"test","temperature":%s}'%(datetime.datetime.utcnow().isoformat(),temperature+i) for i in range(5)]
		packs="["+",".join(pack)+"]"
                packs = d.getpacket(pack[0])
		#print packs[0]
		#continue
                import json
                packs[0]["deviceid"]="name%s" % (mid%2)
		#(rc, mid) = mwpub(json.dumps(packs[0]))
                imu_sensor_data["timestamp"]=datetime.datetime.utcnow().isoformat()
                (rc,mid) = mwpub(json.dumps(imu_sensor_data))
		time.sleep(delay)
