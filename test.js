var gdax = require('gdax');
var publicClient = new gdax.PublicClient('BTC-USD');
var fs = require('fs');

/* publicClient.getProducts((error, response, data) => {
  if (error) {
    console.log(error);
  } else {
    console.log(data);
  }
}); */

(function (){
	var timeout = setInterval(function(){
		publicClient.getProductTicker(function(err, response, data) {
		//console.log(err);
		//console.log(data);
	
		console.log(data.price);
		console.log(data.time);
	
		fs.appendFileSync('data.csv',data.price + ',');
		fs.appendFileSync('data.csv',data.time + '\n');
		});
	},10000);
}) ();
