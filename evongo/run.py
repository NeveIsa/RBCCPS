from eve import Eve
import dateutil.parser

def before_insert(resource_name, items):
  print "\n",items,"\n"
  for item in items:
    try:
      #item['name']='sampad'
      item['timestamp']=dateutil.parser.parse(item['timestamp'])
    except:
      print "Exception ---> timestamp field not found"
  print('About to store items to "%s" ' % resource_name)

app = Eve()
app.on_insert += before_insert

if __name__ == '__main__':
    app.run()
