var express  = require('express');
var app      = express();



mqtt = require("mqtt");
var mqttclient  = mqtt.connect('mqtt://localhost')

const bodyParser = require('body-parser');
app.use(bodyParser.text({ inflate: true, type: '*/*' }))
//
//app.use(bodyParser.urlencoded({ extended: false }));
//app.use(bodyParser.json());

var httpProxy = require('http-proxy');
var apiProxy = httpProxy.createProxyServer();
var serverOne = 'http://localhost:9200'

var count=1;



function extract_sensor_data(request_body)
{
	data=request_body.split("\n");
	values=[];
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




app.all("*", function(req, res)
{
    	//apiProxy.web(req, res, {target: serverOne});
	apiProxy.web(req, res, {target: serverOne});

	values=extract_sensor_data(req.body);
	publish(values);

	console.log("\n");
	console.log("-".repeat(50));
	console.log("Requests processed: " + count++ + "\n" );
	for (key in STATS)
	{
		console.log(key + " : " + STATS[key] + " | "  + STATS_LAST_UPDATE[key]);
	}

	res.send('{"status":"ok"}')
});



//var port = process.argv[2]
//console.log("Running on PORT:" + port)
app.listen(9500);
