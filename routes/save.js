var express = require('express');
var router = express.Router();
process.env.PATH = process.env.VIRTUAL_ENV + ";" + process.env.PATH;

var path = require('path');
var pyshell = require('python-shell');

pyshell.defaultOptions = { pythonPath: 'C:\\Users\\joshiu\\python\\venvs\\36-numpy\\scripts\\python', scriptPath: 'C:\\Users\\joshiu\\WebstormProjects\\RegexNLP-app'};
pyshell = new pyshell('test.py', {
    mode: 'json'
}, function (err, results){
    console.log(results)
});
pyshell.on('message', function (message) {
    // received a message sent from the Python script (a simple "print" statement)
    console.log(message);
});

/* Save resource as json */
router.get('/:variable/:class', function(req, res, next) {
    pyshell.send({'function': 'save', 'params': req.params});
    console.log(req.toString());
    console.log(req.params);
    res.send(req.params);
});

module.exports = router;
