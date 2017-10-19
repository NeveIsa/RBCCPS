from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    status=open("status.txt").read()
    return open("index.html").read().format(status)



app.run(port=80)
