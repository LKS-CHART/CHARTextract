var express = require('express');
var router = express.Router();
var pyshell_connector = require("../python_connector/connector");
var path = require('path');
var prog_status = null;
var settings_path = path.join(__dirname,"..","public","data","project_settings.json");

//console.log(settings_path);

router.get('/get_response_status', function(req, res, next) {
    res.send(JSON.stringify(prog_status, null, 4))
});

/*
router.get('/get_paths', function(req, res, next) {
    console.time("dbsave");

    pyshell_connector.send({'function': 'paths'});
    var curPromise = new Promise(function (resolve, reject) {
        pyshell_connector.on('message', function(message) {resolve(message)});
    });
    curPromise.then(function (result) {
        console.log(result);
        res.send(result)
    });
});
*/

router.get('/get_cwd', function(req, res, next){
    pyshell_connector.send({'function': 'get_cwd'});
    var curPromise = new Promise(function (resolve, reject){
        pyshell_connector.on('response', function(message) {resolve(message)});
    });

    curPromise.then(function (result){
        res.send(result)
    });
});

router.get('/:variable', function(req, res, next) {
    console.time("dbsave");
    //console.log(req.params);
    req.params["settings"] = settings_path;

    pyshell_connector.send({'function': 'run_variable', 'params': req.params});
    var curPromise = new Promise(function (resolve, reject) {
        pyshell_connector.on('response', function(message) {resolve(message)});
    });
    curPromise.then(function (result) {
        console.log("Run variable result: " + result['message']);
        prog_status = result;
        res.redirect("/")
    });
});


module.exports = router;
