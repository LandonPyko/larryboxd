const http = require('http');
const mysql = require('mysql');
const express = require('express');

var con = mysql.createConnection({
  host : "localhost",
  user: "username",
  password: "password"
});

con.connect(function(err) {
  if (err) throw err;
  console.log("Connected");
  con.query("CREATE DATABASE mydb", function (err, result) {
    if (err) throw err;
    console.log("Database created");
  });
  con.query(sql, function (err, result) {
    if (err) throw err;
    console.log("Result: " + result);
  });
});


//http.createServer(function (req, res) {
    //res.writeHead(200, {'Content-Type': 'text/plain'});
    //res.write('Hello World!');
    //res.end();
  //}).listen(8080);  
