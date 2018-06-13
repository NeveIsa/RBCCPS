import json,requests
from datetime import datetime
from elasticsearch import Elasticsearch
import sys 

#GLOBALS
_CONF=json.loads(open("_mwconf.json").read())
ES_HOST="{}:9200".format(_CONF["ip"])

POOL_SIZE=_CONF["pool_size"]
ES_INDEX_PREFIX=_CONF["es_index_prefix"]

# do not use prefix as *helloworld is more expensive for elastic than helloworld*
# Also use YYYY-MM-DD format as helloworld-2018* will give for whole year,
# helloworld-2018-01* will give for Jan 2018 , etc and is easy and light on elastic than the format DD-MM-YYYY

#ES_INDEX_DATE_POSTFIX=lambda:datetime.now().strftime("%Y-%m-%d")
ES_INDEX_DATE_POSTFIX=lambda :"test"
DOC_TYPE="middlewaredata"
es = Elasticsearch(ES_HOST,maxsize=POOL_SIZE)


s=requests.Session()
def publish(payload,using_requests=False,using_requests_session=False,bulk=False,debug=False):
  try:
    if not using_requests:
      payload=json.loads(payload)
  except:
    print("Payload is not a valid JSON... ES Publish Failed")
    return False

  ES_INDEX=ES_INDEX_PREFIX+ "-"  +ES_INDEX_DATE_POSTFIX()

  print ES_INDEX,datetime.utcnow(),
  sys.stdout.write("\r")
  sys.stdout.flush()
  
  if using_requests:
    URL="http://"+ES_HOST+"/"+ES_INDEX+"/"+DOC_TYPE
    if bulk:
      URL="http://"+ES_HOST+"/"+ES_INDEX+"/"+DOC_TYPE+"/_bulk"
    #print (URL)
    if using_requests_session:
      result=s.post(url=URL,data=payload,headers={"content-type":"application/json"}) 
    else:
      result=requests.post(url=URL,data=payload,headers={"content-type":"application/json"})

    if debug:
      print "\nSTATUS_CODE:",result.status_code
      print "RESULT.TEXT:\n",result.text,"\n"
      
    
    if result.ok:
      return True
    else:
      return False

  # donot use es.create as it requires a id parameter to be supplied manually instead of auto generating it like in the case of es.index method
  else:
    es.index(index=ES_INDEX,doc_type=DOC_TYPE,body=payload)
  return True


def rpublish(payload,**kwargs):
  return publish(payload,True,**kwargs)

def spublish(payload,**kwargs):
  return publish(payload,True,True,**kwargs)


if __name__=="__main__":
  import gevent,time,requests
  from gevent import monkey
  from gevent.pool import Pool as ThreadPool

  pool=ThreadPool(POOL_SIZE)

  N_REQ=_CONF["test_NREQ"]
  print "Making",N_REQ,"requests using various methods to post to elasticsearch DB...\n"


  start=time.time()
  for _ in range(N_REQ):
    publish('{"hello":"world"}')
  sys.stdout.write(" "*80)
  sys.stdout.write("\r")
  sys.stdout.flush()
  print "Using elasticsearch (FOR LOOP) library\n(Fails using monkey_patch, more work needed to figure out why)\n",time.time()-start,"\n"


  start=time.time()
  for _ in range(N_REQ):
    rpublish('{"hello":"world"}')
  sys.stdout.write(" "*80)
  sys.stdout.write("\r")
  sys.stdout.flush()
  print "Using requests (FOR LOOP)\n",time.time()-start,"\n"


  start=time.time()
  for _ in range(N_REQ):
    gevent.spawn(rpublish,'{"hello":"world"}')
  gevent.wait()
  sys.stdout.write(" "*80)
  sys.stdout.write("\r")
  sys.stdout.flush()
  print "Using request (GEVENT) without monkey patching [gevent.spawn each loop] \n",time.time()-start,"\n"


  print "Monkey patching...",
  monkey.patch_all()
  print "Monkey patched\n"

  start=time.time()
  for _ in range(N_REQ):
    gevent.spawn(rpublish,'{"hello":"world"}')
  gevent.wait()
  sys.stdout.write(" "*80)
  sys.stdout.write("\r")
  sys.stdout.flush()
  print "Using request (GEVENT) with monkey patching [gevent.spawn each loop] \n",time.time()-start,"\n"


  start=time.time()
  for _ in range(N_REQ):
    pool.apply_async(rpublish,('{"hello":"world"}',))
  pool.join()
  sys.stdout.write(" "*80)
  sys.stdout.write("\r")
  sys.stdout.flush()
  print "Using request (GEVENT) with monkey patching with %s greenthreads using  gevent.pool\n" % POOL_SIZE,time.time()-start,"\n"



