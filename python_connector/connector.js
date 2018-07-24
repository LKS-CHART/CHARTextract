process.env.PATH = process.env.VIRTUAL_ENV + ";" + process.env.PATH;

let path = require('path');
let pyshell = require('python-shell');
pyshell.defaultOptions = { pythonPath: path.resolve(__dirname, "..", "RegexNLP-py", "RegexNLP.exe")};
//pyshell.defaultOptions = { pythonPath: "C:\\PycharmProjects\\NgramRegexNLP\\dist\\RegexNLP\\RegexNLP.exe"};
pyshell = new pyshell("", {
    mode: 'json'
}, function (err, results){
    console.log(results);
});

module.exports = pyshell;