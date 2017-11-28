var gdax = require('gdax');
var publicClient = new gdax.PublicClient('LTC-USD');
//var publicClient = new gdax.PublicClient('BTC-USD');
var fs = require('fs');
http = require('http'),
url = require('url'),
XMLHttpRequest = require('xmlhttprequest').XMLHttpRequest;

var gdaxObData, krakenObData, poloniexObData;

/* publicClient.getProducts((error, response, data) => {
  if (error) {
    console.log(error);
  } else {
    console.log(data);
  }
}); */
function getDayName(dateStr, locale)
{
    var date = new Date(dateStr);
    return date.toLocaleDateString(locale, { weekday: 'long' });
}

function getDayNum(dayStr){
	if (dayStr == 'Sunday'){
		return 0;
	}
	else if (dayStr == 'Monday'){
		return 1;
	}
	else if (dayStr == 'Tuesday'){
		return 2;
	}
	else if (dayStr == 'Wednesday'){
		return 3;
	}
	else if (dayStr == 'Thursday'){
		return 4;
	}
	else if (dayStr == 'Friday'){
		return 5;
	}
	else if (dayStr == 'Saturday'){
		return 6;
	}
}

function ultimateCallback(gdaxResponseHandled, krakenResponseHandled, poloniexResponseHandled, gdaxObData, krakenObData, poloniexObData){
	if(gdaxResponseHandled && krakenResponseHandled && poloniexResponseHandled){
		fs.appendFileSync(fileName, gdaxObData + '?');
		fs.appendFileSync(fileName, krakenObData + '?');
		fs.appendFileSync(fileName, poloniexObData + '\n');
	}
}

function handleMisses(gdaxResponseHandled, krakenResponseHandled, poloniexResponseHandled){
	if(!gdaxResponseHandled || !krakenResponseHandled || !poloniexResponseHandled){
		fs.appendFileSync(fileName, gdaxObData + '?');
		fs.appendFileSync(fileName, krakenObData + '?');
		fs.appendFileSync(fileName, poloniexObData + '\n');
	}
} 

// create new file name
var date = new Date();
var fileName = "gdax_" + date.getMonth() + "_" + date.getDate() + "_" + date.getFullYear() + ".csv"
// Add headers
fs.appendFileSync(fileName, 'TIME?');
fs.appendFileSync(fileName, 'PRICE?');
fs.appendFileSync(fileName, 'GdaxOb?');
fs.appendFileSync(fileName, 'KrakenOb?');
fs.appendFileSync(fileName, 'PoloniexOb\n');

var gdaxResponseHandled,
	krakenResponseHandled,
	poloniexResponseHandled;

var i = 0;
(function (){
var timeout = setInterval(function(){
	console.log("\niterated");
	
	handleMisses(gdaxResponseHandled,krakenResponseHandled, poloniexResponseHandled);
	
	gdaxResponseHandled = false;
	krakenResponseHandled = false;
	poloniexResponseHandled = false;
	
	
	
	publicClient.getProductTicker(function(err, response, data) {
		
		//console.log(data.time);
		//var date_str = data.time.match(/(^[0-9]*-[0-9]*-[0-9]*)/).toString().split(',')[0]
		//var time = data.time.match(/[0-9]*:[0-9]*:[0-9]*/).toString()
		//var day = getDayNum(getDayName(date_str, "en-US"))
		//var hour_length = time.match(/^[0-9]*:/).toString().length
		//var hour = time.match(/^[0-9]*:/).toString().substring(0,hour_length - 1).toString()
		//var minute = time.match(/:[0-9]*:/).toString().substring(1,3)
		
		var time = new Date().getTime();
		fs.appendFileSync(fileName,time + '?');
		fs.appendFileSync(fileName,data.price + '?'); 
		
		// GDAX OB
		publicClient.getProductOrderBook({'level': 2}, function(err, response, data) {
			data.exchange="GDAX";
			gdaxObData = JSON.stringify(data);
			console.log("GDAX");
			gdaxResponseHandled = true;
			ultimateCallback(gdaxResponseHandled, krakenResponseHandled, poloniexResponseHandled, gdaxObData, krakenObData, poloniexObData);
		});	
		
		// KRAKEN OB
		xmlhttp = new XMLHttpRequest();
		xmlhttp.onreadystatechange=function(){
			if (xmlhttp.readyState==4 && xmlhttp.status==200 && !krakenResponseHandled){
				string=xmlhttp.responseText;
				krakenJson = JSON.parse(string);
				krakenJson.exchange = "KRAKEN";
				string = JSON.stringify(krakenJson);
				krakenObData = string;
				krakenResponseHandled = true;
				console.log("kraken");
				ultimateCallback(gdaxResponseHandled, krakenResponseHandled, poloniexResponseHandled, gdaxObData, krakenObData, poloniexObData);
			}
		}	
		xmlhttp.open("GET","https://api.kraken.com/0/public/Depth?pair=LTCUSD&count=50", true);
		xmlhttp.send();
		
		// POLONIEX OB
		poloxmlhttp = new XMLHttpRequest();
		poloxmlhttp.onreadystatechange=function(){
			if (poloxmlhttp.readyState==4 && poloxmlhttp.status==200 && !poloniexResponseHandled){
				string=poloxmlhttp.responseText;
				JSONobj = JSON.parse(string);
				JSONobj.exchange = "POLONIEX";
				string = JSON.stringify(JSONobj);
				poloniexObData = string;
				poloniexResponseHandled = true;
				console.log("poloniex");
				ultimateCallback(gdaxResponseHandled, krakenResponseHandled, poloniexResponseHandled, gdaxObData, krakenObData, poloniexObData);
			}
		}
		poloxmlhttp.open("GET","https://poloniex.com/public?command=returnOrderBook&currencyPair=USDT_LTC&depth=50", true);
		poloxmlhttp.send();
			
		

	});
	
	
	
	/* if(i < 360){
		i++;
	} 
	else{
		process.exit();
	} */
},10000);
}) ();
