var express = require('express');
var router = express.Router();
var pyshell = require('../python_connector/connector');
var fs = require("fs");
var path = require("path");
let out_rules_path = "Z:\\LKS-CHART\\Projects\\NLP POC\\Study data\\TB\\dev\\rules\\tb_rules";
//rules_path = "Z:\\GEMINI-SYNCOPE\\NLP Validation Project\\training\\fixed set\\Regexes";

router.post('/:variable/:class', function(req, res, next) {

    var filePath = path.join(out_rules_path, req.params['variable'], req.body.filename);
//    filePath = path.join(filePath, req.body.filename)
    fs.writeFile(filePath, req.body.regexes, function(err) {
        if(err) {
            return console.log(err)
        }

        console.log("Saved")
    });
    console.log("Received save");
    console.log(req.params);
    console.log(req.body);
    res.sendStatus(200);
});

router.post('/save_project_settings', function(req, res, next) {
    var filePath = "./public/data/project_settings.json";

    fs.writeFile(filePath, JSON.stringify(req.body["Project Settings Data"], null, 4), function(err) {

        if(err) {
            return console.log(err)
        }

        console.log("Save Settings");
        console.log(req.body);
        res.sendStatus(200);
    })

});

module.exports = router;
