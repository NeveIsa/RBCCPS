#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import datetime
import json

CONFIG_DIR = "/home/raghu/Desktop/configFiles"
LAST_SCANNED = 0
MODBUS_CONFIG = {}
MAX_NO_POLLS = 500 # @115200 its ~750

def findConfFiles(_dir):
    global CONFIG_DIR, LAST_SCANNED
    if os.path.exists(_dir) :
        #print("Config files' path found.")
        confFiles=os.listdir(_dir)
        confFiles=filter(lambda x:x.endswith(".conf"),confFiles)
        confFiles=list(confFiles)
        #print (confFiles)
        return confFiles
    else:
        print("Config files' path NOT found:",_dir)
        
        
    
def isFileUpdated(_filename):
    fPath = CONFIG_DIR+"/"+_filename
    if LAST_SCANNED < os.path.getmtime(fPath):
        return True
    else:
        return False
    
def readConfigFile(_filename):
    fPath = CONFIG_DIR+"/"+_filename
    with open(fPath) as f:
        conf = f.read()
    try:
        conf=json.loads(conf)
        return conf
    except Exception as e:
        print(e)
    
            
    

def main():
    global LAST_SCANNED, MODBUS_CONFIG
    confFiles=findConfFiles(CONFIG_DIR)
    tempTime = int(time.time())
    print("Files found:\n--> "+"\n--> ".join(confFiles)+"\n" )
    for curFile in confFiles:
        if isFileUpdated(curFile):
            print("Found modified:", curFile)
            MODBUS_CONFIG[curFile]=readConfigFile(curFile)
        else:
            print("Found unmodified:", curFile)
            
            
            
    LAST_SCANNED = tempTime
    print(MODBUS_CONFIG)
    
if __name__ =="__main__":
    while (1):
        main()
        print("====="*10)
        time.sleep(10)
        
