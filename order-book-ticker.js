var gdax = require('gdax');
var publicClient = new gdax.PublicClient('LTC-USD');
var fs = require('fs');

//(function (){
	//var timeout = setInterval(function(){
		publicClient.getProductOrderBook({'level': 2}, function(err, response, data) {
		console.log(err);
		console.log(data);
	
		console.log(data.price);
		console.log(data.time);
	
		fs.appendFileSync('orderBookData.csv',data.price + ',');
		fs.appendFileSync('orderBookData.csv',data.time + '\n');
		});
//	},300000);
//}) ();