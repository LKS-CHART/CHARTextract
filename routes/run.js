var express = require('express');
var router = express.Router();
var pyshell_connector = require("..\\python_connector\\connector");
/* Save resource as json */


pyshell = new pyshell_connector('__main__.py', {
    mode: 'json'
}, function (err, results){
    console.log(results)
});

let x = 0;

let test = function(message) {
    if (message['status'] === 200){
        resolve(message);
    } else {
        reject("404");
    }
};
let runPromise = function() {
    pyshell.on('message', message => test(message));
    return new Promise((resolve, reject) => {

    })
};


router.get('/:variable', function(req, res, next) {
    console.time("dbsave");
    console.log(req.params);


    pyshell.send({'function': 'run_variable', 'params': req.params});


    x = x + 1;
    Promise.all([runPromise]).then(function (message) {
        res.redirect("http://localhost:8080/NgramRegexNLP/generated_data/diagnosis/train/index.html");
    });
});

module.exports = router;
