"""
Make sure /etc/elasticsearch/elasticsearch.yml has
 the repo.path setup matching the _esconfig.json.

Make sure this repo.path directory is owned by both
 elasticsearch user and group

"""

import requests,json,datetime,time
import os

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
ES_REPOPATH=ES_CONF["repo.path"]

ES_URL="http://{}:{}".format(ES_HOST,ES_PORT)


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

    def restore(self,index):
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
        cmd="sudo rm {}/*".format(self.repodir)
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
    repo.snapshot_yesterday("helloworld")
    repo.status()

