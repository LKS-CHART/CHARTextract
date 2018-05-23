process.env.PATH = process.env.VIRTUAL_ENV + ";" + process.env.PATH;

var path = require('path');
var pyshell = require('python-shell');

pyshell.defaultOptions = { pythonPath: 'C:\\Users\\joshiu\\python\\venvs\\36-numpy\\scripts\\python',
    scriptPath: 'C:\\Users\\joshiu\\PyCharmProjects\\NgramRegexNLP'};
pyshell = new pyshell('__main__.py', {
    mode: 'json'
}, function (err, results){
    console.log(results)
});

module.exports = pyshell;