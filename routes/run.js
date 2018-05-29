var express = require('express');
var router = express.Router();
var pyshell_connector = require("..\\python_connector\\connector");
/* Save resource as json */

pyshell = new pyshell_connector('__main__.py', {
    mode: 'json'
}, function (err, results){
    console.log(results)
});

router.get('/:variable', function(req, res, next) {
    console.time("dbsave");
    console.log(req.params);

    pyshell.send({'function': 'run_variable', 'params': req.params});
    let curPromise = new Promise(function (resolve, reject) {
        pyshell.on('message', function(message) {resolve(message)});
    });
    Promise.all([curPromise]).then(function (result) {
        res.redirect("http://localhost:8080/NgramRegexNLP/generated_data/diagnosis/train/index.html");
    });
});

module.exports = router;
