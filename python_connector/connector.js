process.env.PATH = process.env.VIRTUAL_ENV + ";" + process.env.PATH;

let path = require('path');
let pyshell = require('python-shell');

pyshell.defaultOptions = { pythonPath: 'C:\\Users\\joshiu\\python\\venvs\\36-numpy\\Scripts\\python',
    scriptPath: 'C:\\Users\\joshiu\\PyCharmProjects\\NgramRegexNLP'};

pyshell = new pyshell('__main_simple__.py', {
    mode: 'json'
}, function (err, results){
    console.log(results);
});

module.exports = pyshell;