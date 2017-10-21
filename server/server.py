import os
from flask import Flask,redirect
import uuid



gformurl=open("gformurl.txt").read()
import requests
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
gform_doc=requests.get(gformurl,headers=headers).text

from bs4 import BeautifulSoup
soup = BeautifulSoup(gform_doc, 'html.parser')

for x in soup.findAll("script"):
  x.decompose()

with open("gform.html",'w') as g:
  g.write(str(soup))

app = Flask(__name__)

@app.route("/")
def index():
  if os.path.exists("recordID.txt"):
    recordID=open("recordID.txt").read()
  else:
    recordID=str(uuid.uuid4())
    with open("recordID.txt",'w') as g:
      g.write(recordID)


  status=open("status.txt").read().strip()
  recordIDscript="<script>var recordID='{0}'\nvar jobStatus='{1}'</script>".format(recordID,status)
  template=open("header.html").read()+open("gform.html").read()+recordIDscript+open("footer.html").read()
 
  
  return template
  
@app.route("/currentJob")
def showCurrentJob():
  recordID=open("recordID.txt").read()
  return "<style>body{background-color:blue;}</style><h2 style='color:white;'>Current job has started with  recordID: %s </h2>" % recordID

#@app.route("/record")
#def record(recordID):


app.run(port=80)
