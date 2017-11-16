var http = require('http'),
fs = require('fs'),
url = require('url'),
XMLHttpRequest = require('xmlhttprequest').XMLHttpRequest;
	 
xmlhttp = new XMLHttpRequest();
xmlhttp.open("GET","https://api.kraken.com/0/public/Depth?pair=LTCUSD", true);
xmlhttp.onreadystatechange=function(){
    if (xmlhttp.readyState==4 && xmlhttp.status==200){
        string=xmlhttp.responseText;
		console.log(string);
    }
}
xmlhttp.send();
