process.env.PATH = process.env.VIRTUAL_ENV + ";" + process.env.PATH;

let path = require('path');
let pyshell = require('python-shell');

pyshell.defaultOptions = { pythonPath: 'C:\\Users\\MathewSh\\anaconda3\\python',
    scriptPath: 'C:\\Users\\MathewSh\\PyCharmProjects\\NgramRegexNLP'};

pyshell = new pyshell('__main_simple__.py', {
    mode: 'json'
}, function (err, results){
    console.log(results);
});

module.exports = pyshell;