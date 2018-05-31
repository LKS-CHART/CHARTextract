let express = require('express');
let router = express.Router();
let pyshell_connector = require("..\\python_connector\\connector");
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
        var redirect_url = "http://localhost:8080/NgramRegexNLP/generated_data/" + req.params.variable +  "/train/index.html";
        res.redirect(redirect_url);
    });
});

module.exports = router;
