process.env.PATH = process.env.VIRTUAL_ENV + ";" + process.env.PATH;

let path = require('path');
let pyshell = require('python-shell');

pyshell.defaultOptions = { pythonPath: 'C:\\Users\\joshiu\\python\\venvs\\36-numpy\\scripts\\python',
    scriptPath: 'C:\\Users\\joshiu\\PyCharmProjects\\NgramRegexNLP'};


module.exports = pyshell;