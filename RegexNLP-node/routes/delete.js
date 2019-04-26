var express = require('express');
var router = express.Router();
var fs = require("fs");
var path = require("path");
var filePath = "./public/data/project_settings.json";
var save = require("./save");

router.post('/:variable/:class', function(req, res, next) {
    console.log("Received Delete");
    if (save.rules_path === null) {
        console.log("No Rules Path Specified");
        res.sendStatus(404);
    }

    console.log(save.rules_path);
    console.log(req.body.filename);
    console.log(req.body);
    var filePath = path.join(save.rules_path, req.params['variable'], req.body.filename);
    var index = req.body.filename.indexOf(".txt");
    var jsonFileName = req.body.filename.substring(0,index) + ".json";
    var jsonFilePath = path.join(save.rules_path, req.params["variable"], jsonFileName)

    fs.unlinkSync(filePath);
    fs.unlinkSync(jsonFilePath);

    res.sendStatus(200);
});

module.exports = router;
