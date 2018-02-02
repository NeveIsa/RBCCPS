
if(location.href.indexOf("kibana")!=-1)
{


el=$(".global-nav-link").eq(-2)

elnew=el.clone()

elnew.removeAttr("ng-click")
elnew.removeAttr("aria-label")
elnew.removeAttr("href")
elnew.removeAttr("data-test-subj")

elnew.find(".global-nav-link__title").html("<b>Download</b>")

elnew.find(".global-nav-link__icon-image").attr("src","/plugins/kibana/assets/play-circle.svg")
elnew.find(".global-nav-link__icon-image").removeAttr("ng-if")
elnew.find(".global-nav-link__icon-image").removeAttr("kbn-src")
elnew.find(".global-nav-link__icon-image").removeAttr("aria-hidden")


elnew.find("a").removeAttr("href")
elnew.find("a").removeAttr("ng-click")
elnew.find("a").removeAttr("aria-label")
elnew.find("a").removeAttr("data-test-subj")

elnew.css("background-color","brown")

elnew.click(downloader)

el.after(elnew)




}

function downloader(argument) {
	console.log($("pre[data-test-subj='visualizationEsRequestBody']").html())
}