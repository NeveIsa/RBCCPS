import json

data=open("response_reg.txt").read()

data=data.strip().split("\n")

if "200 OK" in data[0]:
  details=json.loads(data[-1])
  if details["Registration"]=="success":
    print details
  else:
    print "Failed to register the new device... Exiting..."
    raise Exception
else:
  print "Failed to register the new device... Exiting..."
  raise Exception
