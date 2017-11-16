var http = require('http'),
fs = require('fs'),
url = require('url'),
XMLHttpRequest = require('xmlhttprequest').XMLHttpRequest;	 
	 
xmlhttp = new XMLHttpRequest();
xmlhttp.open("GET","https://poloniex.com/public?command=returnOrderBook&currencyPair=USDT_LTC&depth=10", true);
xmlhttp.onreadystatechange=function(){
    if (xmlhttp.readyState==4 && xmlhttp.status==200){
        string=xmlhttp.responseText;
		console.log(string);
    }
}
xmlhttp.send();
