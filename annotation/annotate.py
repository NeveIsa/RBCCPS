import requests
import yaml
import requests
import datetime

with open("conf.yml") as f:
    conf=f.read()
    CONF=yaml.load(conf)
    ESHOST,ESPORT,ESINDEX=CONF['eshost'],CONF['esport'],CONF['esindex']
    EVENTS=CONF['events']


URL = "http://{}:{}/{}/mytype/".format(ESHOST,ESPORT,ESINDEX)
#print(URL)


def listevents():
    for k,v in EVENTS.items():
        print ("{} | {}".format(k,v) )


def askevent():
    print("Enter event key",end=": ")
    k=input()
    try:
        key=int(k)
    except Exception as e:
        print("----------------------> converting key to int failed.")
        return None
    if not key in EVENTS.keys():
        print("----------------------> key not found.\n")
        return None
    event=EVENTS[key]
    if key==0:
        print("Enter event description",end=": ")
        description=input()
        event+=": " +description
    #print("---> Logging:",event)
    return event


def sendevent(e):
    now=datetime.datetime.utcnow().isoformat()
    payload={'event':e,'timestamp':now}
    with open("events.csv",'a') as g:
        g.write("%s,%s\n" % (now,e))
    print("---> logging: {} | {}\n".format(e,now))
    requests.post(URL,json=payload)


if __name__=="__main__":
    import os

    if not os.path.exists("events.csv"):
        print("---> creating events.csv")
        os.system("echo timestamp,event > events.csv" )
    
    
    
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1]=='test':
            pass

    else:
        while True:
            listevents()
            ev=askevent()
            if not ev==None: sendevent(ev)

