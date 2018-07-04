var express = require('express');
var router = express.Router();
var pyshell_connector = require("..\\python_connector\\connector.js");
var path = require('path');
var prog_status = null;
settings_path = path.join(__dirname,"..","public","data","project_settings.json");

console.log(settings_path);

router.get('/get_response_status', function(req, res, next) {
    res.send(JSON.stringify(prog_status, null, 4))
})

router.get('/:variable', function(req, res, next) {
    console.time("dbsave");
    console.log(req.params);
    req.params["settings"] = settings_path;

    pyshell_connector.send({'function': 'run_variable', 'params': req.params});
    var curPromise = new Promise(function (resolve, reject) {
        pyshell_connector.on('message', function(message) {resolve(message)});
    });
    Promise.all([curPromise]).then(function (result) {
        prog_status = result;
        res.redirect("/")
    });
});

module.exports = router;
