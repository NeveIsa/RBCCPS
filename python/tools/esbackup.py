"""
Make sure /etc/elasticsearch/elasticsearch.yml has
 the repo.path setup correctly.

Make sure this repo.path directory is owned by both
 elasticsearch user and group

"""

import requests,json,datetime,time
import os,yaml,sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


ES_CONF=json.loads(open("_esconf.json").read())

ES_HOST=ES_CONF['ip']
ES_PORT=ES_CONF['port']

ES_CONF_FILE=yaml.load(open(ES_CONF["configfile"]))

ES_REPOPATH=ES_CONF_FILE["path.repo"][0]

ES_URL="http://{}:{}".format(ES_HOST,ES_PORT)

print "FOUND REPO PATH AS ---> " + ES_REPOPATH
print bcolors.WARNING + "Is this the intened path?" + bcolors.FAIL + "  !!! Consequences could be severe if wrong path... y/N" + bcolors.ENDC,

if raw_input().upper()!="Y":exit()


class Repo:
    def __init__(self,reponame="backup",repodir=ES_REPOPATH):
        self.reponame=reponame
        self.repodir=repodir

    def register(self):
        """
        PUT /_snapshot/backup
        """

        url = ES_URL + "/_snapshot/{}".format(self.reponame)

        putdata = \
        {\
            "type": "fs",\
            "settings": { "location": "{}".format(self.repodir)}\
        }

        result=requests.put(url,data=json.dumps(putdata),headers={"Content-type":"application/json"})
        print "register_repo ->",

        if result.ok:
            print result.text
            print "GET {} -->".format(ES_URL),
            print requests.get(url).text
        else:
            print "failed"

        print ""

    def snapshot(self,index):

        """
        PUT /_snapshot/{{reponame}}/snapshot
        {
            "indices": "helloworld-2018-01-05"
        }

        """

        url=ES_URL+"/_snapshot/{}/snapshot".format(self.reponame)

        putdata=\
        {\
            "indices": "{}".format(index)\
        }\

        result=requests.put(url,data=json.dumps(putdata),headers={"Content-type":"application/json"})
        print result.text

    def restore(self):
        """
        POST /_snapshot/{{reponame}}/snapshot/_restore
        """

        url=ES_URL+"/_snapshot/{}/snapshot/_restore".format(self.reponame)
        result=requests.post(url)
        if result.ok:
            print "RESTORE SUCCESSFULL..."
        else:
            print "RESTORE FAILED..."
        print result.text


    def check_restore_progress(self,index=""):
        url=ES_URL + "/_cat/recovery"
        import re,time

        timeout=20

        while True:
            results=requests.get(url)
		
	    # If index="", try to auto detect
	    if index=="":
		tempIndex=[]
		print "\n---> AUTO DETECTING INDEX NAME FOR ANY RESTORE CURRENTLY IN PROGRESS..... HOLD TIGHT"
		for line in results.text.split("\n"):
		    line=line.strip()
		    if "backup" in line and "snapshot" in line and not "done" in line:
			print line
			temp=line.split(" ")[0]
			print "---> DETECTED :",temp
			tempIndex+=[temp]
		
		if len(tempIndex)==0:
			print "\nNO MATCH FOUND... WAITING {}s".format(timeout)
			time.sleep(1)
			timeout-=1
			continue # continue while loop

		if len(set(tempIndex))==1:
			index=list(set(tempIndex))[0]
			print "\nSUCCESSFULLY DETECTED INDEXNAME : {}".format(index)
		else:
			print "\nMORE THAN ONE SUITABLE CANDIDATES, COULDN'T ARBITRATE.... EXITING"
			print set(tempIndex)
			return 1 # 1=error,0=all good
			
		

            sr=re.search(index,results.text)

            if sr:
                print "\nFound indexname {} in restore logs".format(index)
                break
            else:
                print "\nThe restore progress log doesn't contain any trace of the indexname {}".format(index)
                print "waiting ... {}".format(timeout)
                time.sleep(1)
                timeout-=1
                if timeout==0:
                    break

	time.sleep(1)
	lines = results.text.split("\n")

	done=1

        for line in lines:
	    line=line.strip()
            lsr=re.search(index,line)
            if lsr:
		if re.search("done",line):
	            print line,"---> DONE"
		else:
		    print line, "---> WAITING"
		    done=0

	if done:
		print "\n---> RESTORE COMPLETED"
		return 0
	else:
		print "\n---> RESTORE IN PROGRESS"
		return 1
		           



    def snapshot_yesterday(self,index_prefix):
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        yesterday=yesterday.strftime("%Y-%m-%d")
        index=index_prefix + "-" + yesterday
	print "YESTERDAY'S INDEX --> " + index,"\n"
        self.snapshot(index)

    def status(self,wait=True): 
        
        url=ES_URL+"/_snapshot/{}/snapshot".format(self.reponame)
        
        try:
            while wait:
                result=requests.get(url)
                reply=json.loads(result.text)
                status=reply["snapshots"][0]["state"]
                print "repo status ->",status
                if status=="SUCCESS":break
                time.sleep(1)
        except Exception as e:
            print "Exception in Repo.status",e

    def clean(self,force=False):
        if not os.path.exists(self.repodir):
            print "Creating repo dir: {}".format(self.repodir)
            os.mkdir(self.repodir)
            cmd="sudo chown {}:{} {}".format("elasticsearch","elasticsearch",self.repodir)
            print "Executing: {}".format(cmd)
            os.system(cmd)
            force=True

        print bcolors.WARNING+"WARNING : {} will be WIPED.".format(self.repodir)+bcolors.ENDC
        cmd="sudo rm -rf {}/*".format(self.repodir)
        print "execute {}{}{} ? : y/N".format(bcolors.FAIL,cmd,bcolors.ENDC),
        
        if force or raw_input()=='Y':
            print "\n"
            os.system(cmd)
            time.sleep(1)

    def check_user(self):
        user=os.popen("whoami").read().strip()
        print bcolors.FAIL+"Current user: %s" % user+bcolors.ENDC
        if not user=="root":
            print "Please run this script as {}{}{}".format(bcolors.FAIL,"root",bcolors.ENDC)


if __name__=="__main__":
    repo=Repo()
    repo.check_user()
    repo.clean(force=True)
    repo.register()
    if len(sys.argv)>1:
        index=sys.argv[1]
        repo.snapshot(index)
    else:
        repo.snapshot_yesterday("helloworld")
    repo.status()

