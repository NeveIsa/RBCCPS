from datetime import datetime
import os,sys


sinceD,sinceM=sys.argv[1].split("-")
sinceD,sinceM=int(sinceD),int(sinceM)


for date in range(30):
    d = date + sinceD
    if d>30:break
    print "date:",d,sinceM
    #os.system("sh backupNcopy.sh helloworld-2018-%s-%s" % (d,sinceM))



