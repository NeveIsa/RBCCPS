import sys
if len(sys.argv)>1 and sys.argv[1]=="gevent":
  from gevent import monkey
  monkey.patch_all(time=False) #donot patch time as we are using it for our CC_DELAY congestion control
  from gevent.pool import Pool as ThreadPool
  print("Using Pool from %s ...\n" % "gevent.pool")
else:
  from multiprocessing.dummy import Pool as ThreadPool
  print("Using Pool from %s ...\n" % "multiprocessing.dummy")


from smartcity import smartcity as scity
#import evongoclient
import elasticclient

import paho.mqtt.subscribe as subscriber 
import json,time

import mqttpub


"""
SMARTCITY_DEVICE_ID="test_SCMWC0"

print "SMARTCITY_DEVICE_ID >",SMARTCITY_DEVICE_ID

print "Available device list..."
print scity.list_devices()


scity_client_device=scity.Device(SMARTCITY_DEVICE_ID);
"""


### CONGESTION CONTROL
CC_DELAY=1 #start slow
CC_DELAY_STEP_SIZE=0.1
CC_DELAY_MAX=10

def CC_STEP_DELAY(steps):
	global CC_DELAY
	CC_DELAY+=steps*CC_DELAY_STEP_SIZE
	if CC_DELAY>CC_DELAY_MAX:
		CC_DELAY=CC_DELAY_MAX
	if CC_DELAY<0:
		CC_DELAY=0

	print("\n-----------------------------------------> CC_DELAY:%s\n" % CC_DELAY)

def CC_WAIT():
	time.sleep(CC_DELAY)


def mwclientthreaded(payload):
	try:
                result=elasticclient.rpublish(payload)
		#result=evongoclient.evongopub(payload)
                #result=scity_client_device.pub(payload)
		if result:
			CC_STEP_DELAY(-5) # recover faster
		else:
			raise
	except:
		mqttpub.mwpub(payload) #Reinsert message into Broker queue
		CC_STEP_DELAY(1)
                import os
                os.system("echo 1 >> log.txt")
	print "\n-----------------------------------------> Uploaded\n",payload,"\n"



#Initialize a pool of worker threads
pool=ThreadPool(70)


while True:
	try:
		msg=subscriber.simple("mwdata",qos=2,client_id="mwclient",clean_session=0)
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
	#pool.apply_async(evongoclientthreaded,(mwpayload,))

	CC_WAIT()






