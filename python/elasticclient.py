import json,requests
from datetime import datetime
from elasticsearch import Elasticsearch


#GLOBALS
ES_HOST="{}:9200".format(json.loads(open("_mwconf.json").read())["ip"])

POOL_SIZE=100
ES_INDEX_PREFIX="helloworld"

# do not use prefix as *helloworld is more expensive for elastic than helloworld*
# Also use YYYY-MM-DD format as helloworld-2018* will give for whole year,
# helloworld-2018-01* will give for Jan 2018 , etc and is easy and light on elastic than the format DD-MM-YYYY
ES_INDEX_DATE_POSTFIX=lambda:datetime.datetime.now().strftime("%Y-%m-%d")

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

  ES_INDEX=ES_INDEX_PREFIX+ES_INDEX_DATE_POSTFIX()

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

  N_REQ=1000
  print "Making",N_REQ,"requests using various methods to post to elasticsearch DB...\n"


  start=time.time()
  for _ in range(N_REQ):
    publish('{"hello":"world"}')
  print "Using elasticsearch (FOR LOOP) library\n(Fails using monkey_patch, more work needed to figure out why)\n",time.time()-start,"\n"


  start=time.time()
  for _ in range(N_REQ):
    rpublish('{"hello":"world"}')
  print "Using requests (FOR LOOP)\n",time.time()-start,"\n"


  start=time.time()
  for _ in range(N_REQ):
    gevent.spawn(rpublish,'{"hello":"world"}')
  gevent.wait()
  print "Using request (GEVENT) without monkey patching\n",time.time()-start,"\n"


  print "Monkey patching...",
  monkey.patch_all()
  print "Monkey patched\n"

  start=time.time()
  for _ in range(N_REQ):
    gevent.spawn(rpublish,'{"hello":"world"}')
  gevent.wait()
  print "Using request (GEVENT) with monkey patching\n",time.time()-start,"\n"


  start=time.time()
  for _ in range(N_REQ):
    pool.apply_async(rpublish,('{"hello":"world"}',))
  pool.join()
  print "Using request (GEVENT) with monkey patching with %s greenthreads using  gevent.pool\n" % POOL_SIZE,time.time()-start,"\n"



