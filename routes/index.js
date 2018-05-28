var express = require('express');
var router = express.Router();
var fs = require('fs');
var path = require('path');
var baseDir = process.env[(process.platform === 'win32') ? 'USERPROFILE' : 'HOME'];

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.get('/path', function(req, res, next) {
  console.log(dirTree(baseDir));
  res.sendStatus(200)
});
module.exports = router;
