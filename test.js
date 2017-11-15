var gdax = require('C:/Program Files/nodejs/node_modules/npm/node_modules/gdax');
var publicClient = new gdax.PublicClient('BTC-USD');

/* publicClient.getProducts((error, response, data) => {
  if (error) {
    console.log(error);
  } else {
    console.log(data);
  }
}); */

publicClient.getProductTicker(function(err, response, data) {
	console.log(err);
	console.log(data);
});