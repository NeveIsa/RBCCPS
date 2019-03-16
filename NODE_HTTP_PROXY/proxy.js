
///////////////////////////////////////////////////////////


const fs= require('fs')
const YAML= require('yaml')



//YAML.parse('3.14159')
// 3.14159
//  
//  YAML.parse('[ true, false, maybe, null ]\n')
//  // [ true, false, 'maybe', null ]
//   
const conf = fs.readFileSync('./conf.yml', 'utf8')
CONF=YAML.parse(conf)
console.log("-----".repeat(10),"Configuration:\n",conf,"\n","-----".repeat(10))


var HITS=0;

mqtt = require("mqtt");
var mqttclient  = mqtt.connect('mqtt://localhost')


function extract_sensor_data(request_body)
{
	data=request_body.split("\n");
	values=[];
	//console.log(data)
	//return;
	for ( indx in data )
	{
		line=data[indx];
		if (line=='{"index":{}}' || line=="");
		else
		{
			//console.log(line);
			//console.log(JSON.parse(line));
			//

			values.push(JSON.parse(line));
		}
	}

	return values;
}



var STATS={};
var STATS_LAST_UPDATE={};
function publish(values)
{
	for ( indx in values)
	{
		val = values[indx];
		devID=val["deviceid"];
		STATS_LAST_UPDATE[devID]=Date();

		if(!(devID in STATS))
		{
			STATS[devID]=1;
		}
		else
		{
				STATS[devID]+=1;
		}

		mqttclient.publish(devID, JSON.stringify(val));
		//
		//console.log(devID);
	}
}


function log_status()
{
		console.log("\n");
		console.log("-".repeat(50));
		console.log("Requests processed: " + HITS++ + "\n" );
		for (key in STATS)
			{
				console.log(key + " : " + STATS[key] + " | "  + STATS_LAST_UPDATE[key]);
			}

}

////////////////////////////////////////////////////////////













var express = require('express')

app=express();

var hpmproxy = require('http-proxy-middleware');

const anyBody = require('body')
function OPR(proxyReq, req, res) {
    anyBody(req, res, function (err, body) {
        if (err) 
	    {
		console.error(err)
		return;
	    }
        //console.log(body)

	values=extract_sensor_data(body);
	publish(values);
	log_status();
    })
}




var options = {
	target: "http://localhost:"+CONF["FORWARD_PORT"],
    	changeOrigin: true, // needed for virtual hosted sites
    	onProxyReq: OPR
};

var hpmApiProxy = hpmproxy(options);
app.use('*', hpmApiProxy);


PORT=CONF["PROXY_PORT"]
console.log("Started proxy on PORT: ",PORT )
app.listen(PORT);
