var express = require('express');
var router = express.Router();
var fs = require("fs");
var path = require("path");
var filePath = "./public/data/project_settings.json";
var save = require("./save")

router.post('/:variable/:class', function(req, res, next) {
    console.log("IN DELETE")
    if (save.rules_path === null) {
        console.log("No Rules Path Specified");
        res.sendStatus(404);
    }

    console.log(save.rules_path)
    console.log(req.body.filename)
    console.log(req.body)
    var filePath = path.join(save.rules_path, req.params['variable'], req.body.filename);
    console.log("HERE")

    fs.unlinkSync(filePath);

    console.log("Received delete");
    res.sendStatus(200);
});

module.exports = router;
