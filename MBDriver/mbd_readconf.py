#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import datetime
import json
import yaml
from pprint import pprint

# Validate YAML per conf file
import cerberus

CONFIG_DIR = "conf.d"
LAST_SCANNED = 0
MODBUS_CONFIG = {}
MAX_NO_POLLS = 500 # @115200 freq. is ~750

def findConfFiles(_dir):
    global CONFIG_DIR, LAST_SCANNED
    if os.path.exists(_dir) :
        #print("Config files' path found.")
        confFiles=os.listdir(_dir)
        confFiles=filter(lambda x:x.endswith(".yaml"),confFiles)
        confFiles=list(confFiles)
        #print (confFiles)
        return confFiles
    else:
        print("Config files' path NOT found:",_dir)
        
        
    
def isFileUpdated(_file):
    if LAST_SCANNED < os.path.getmtime(_file):
        return True
    else:
        return False
    
def readConfigFile(_file):
    with open(_file) as f:
        conf = f.read()
    try:
        conf=yaml.load(conf)
        return conf
    except Exception as e:
        print(e)
    
            
def validateConfigFile(_file):
    with open("schema.yaml") as f:
        schema=f.read()
    
    with open(_file) as f:
        conf=f.read()
    
    schema=yaml.load(schema)
    pprint(schema)
    print ("\n====\n"*2)
    conf=yaml.load(conf)

    v=cerberus.Validator(allow_unknown=False)
    print(v.validate(conf,schema))

    pprint(v.errors)


def main():
    global LAST_SCANNED, MODBUS_CONFIG
    confFiles=findConfFiles(CONFIG_DIR)
    tempTime = int(time.time())
    print("Files found:\n--> "+"\n--> ".join(confFiles)+"\n" )
    for curFile in confFiles:
        curFile = CONFIG_DIR+"/"+ curFile
        validateConfigFile(curFile)
        if isFileUpdated(curFile):
            print("Found modified:", curFile)
            MODBUS_CONFIG[curFile]=readConfigFile(curFile)
        else:
            print("Found unmodified:", curFile)
            
            
            
    LAST_SCANNED = tempTime
    pprint(MODBUS_CONFIG)
    
if __name__ =="__main__":
    while (1):
        main()
        print("====="*10)
        #print("====="*10)
        time.sleep(10)
