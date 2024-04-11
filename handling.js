const http = require('http');
const mysql = require('mysql');
const express = require('express');

http.createServer(function (req, res) {
    res.writeHead(200, {'Content-Type': 'text/plain'});
    res.write('Hello World!');
    res.end();
  }).listen(8080);

