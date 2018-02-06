
if(location.href.indexOf("kibana")!=-1)
{


serverURL="http://localhost:4567"


el=$(".global-nav-link").eq(-2)

dbutton=el.clone()

dbutton.removeAttr("ng-click")
dbutton.removeAttr("aria-label")
dbutton.removeAttr("href")
dbutton.removeAttr("data-test-subj")

dbutton.find(".global-nav-link__title").html("<b>Download</b>")

dbutton.find(".global-nav-link__icon-image").attr("src","/plugins/kibana/assets/play-circle.svg")
dbutton.find(".global-nav-link__icon-image").removeAttr("ng-if")
dbutton.find(".global-nav-link__icon-image").removeAttr("kbn-src")
dbutton.find(".global-nav-link__icon-image").removeAttr("aria-hidden")


dbutton.find("a").removeAttr("href")
dbutton.find("a").removeAttr("ng-click")
dbutton.find("a").removeAttr("aria-label")
dbutton.find("a").removeAttr("data-test-subj")

dbutton.css("background-color","brown")

dbutton.click(downloader)

el.after(dbutton)



function downloader(argument) {
	if(dbutton.attr("active")==="true")
	{
		query=$("pre[data-test-subj='visualizationEsRequestBody']").html()
		
		indexPattern=$("#index_pattern_id").html().trim()

		console.log(indexPattern+"------------->\n\n\n"+query);

		fetch(serverURL +"/"+ indexPattern,
		{
		  method: "POST",
		  body: query
		}
		).then(response=>response.text().then((t)=>{
			//alert(t==query?"successful":"failed")
			console.log(t==query?"successful":"failed")
			console.log("POST_RESPONSE ---> \n" + t)
		}));
	}
	else
	{
		console.log("Not on the right page and/or context")
	}
}


//check if right page and context is found every once in a while
setInterval(()=>
	{
		if($("pre[data-test-subj='visualizationEsRequestBody']").length)
		{
			dbutton.css("background-color","green")
			dbutton.attr("active","true")
		}
		else
		{
			dbutton.css("background-color","brown")
			dbutton.attr("active","false")
		}

	},1000
)



}
