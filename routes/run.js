var express = require('express');
var router = express.Router();
var pyshell_connector = require("..\\python_connector\\connector.js");
var settings_path = "Z:\\LKS-CHART\\Projects\\NLP POC\\Study data\\TB\\dev\\project_settings_tb.json";
var path = require('path');
settings_path = path.join(__dirname,"..","public","data","project_settings.json");

console.log(settings_path);

router.get('/:variable', function(req, res, next) {
    console.time("dbsave");
    console.log(req.params);
    req.params["settings"] = settings_path;

    pyshell_connector.send({'function': 'run_variable', 'params': req.params});
    var curPromise = new Promise(function (resolve, reject) {
        pyshell_connector.on('message', function(message) {resolve(message)});
    });
    Promise.all([curPromise]).then(function (result) {
        var redirect_url = "http://localhost:8080/NgramRegexNLP/generated_data/" + req.params.variable +  "/train/index.html";
        var redirect_url = "/"
        res.redirect(redirect_url);
    });
});

module.exports = router;
