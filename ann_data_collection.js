var gdax = require('gdax');
var publicClient = new gdax.PublicClient('LTC-USD');
//var publicClient = new gdax.PublicClient('BTC-USD');
var fs = require('fs');
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

var i =0;
(function (){
var timeout = setInterval(function(){
	publicClient.getProductTicker(function(err, response, data) {
	console.log(data.time);
	var date_str = data.time.match(/(^[0-9]*-[0-9]*-[0-9]*)/).toString().split(',')[0]
	console.log("Date String: " + date_str)
	var time = data.time.match(/[0-9]*:[0-9]*:[0-9]*/).toString()
	console.log("Time: " + time)
	var day = getDayNum(getDayName(date_str, "en-US"))
	console.log("Day: " + getDayName(date_str, "en-US"))
	var hour_length = time.match(/^[0-9]*:/).toString().length
	var hour = time.match(/^[0-9]*:/).toString().substring(0,hour_length - 1).toString()
	console.log("Hour: " + hour)
	var minute = time.match(/:[0-9]*:/).toString().substring(1,3)
	console.log("Minute: " + minute)
	
	//#place header for file if first write
	if(i == 0){
		fs.appendFileSync('data.csv', 'PRICE,');
		fs.appendFileSync('data.csv', 'DAY,');
		fs.appendFileSync('data.csv', 'HOUR,');
		fs.appendFileSync('data.csv', 'MINUTE\n');
	}
	fs.appendFileSync('data.csv',data.price + ',');
	fs.appendFileSync('data.csv',day + ',');
	fs.appendFileSync('data.csv',hour + ',');
	fs.appendFileSync('data.csv',minute + '\n');
	if(i < 360){
		i++;
	}
	else{
		process.exit();
	}

	});
},5000);
}) ();
