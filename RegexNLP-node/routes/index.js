let express = require('express');
let router = express.Router();
let fs = require('fs');
let path = require('path');
//let baseDir = process.env[(process.platform === 'win32') ? 'USERPROFILE' : 'HOME'];
let appDir = require('../path_helper/paths').getAppRoot();
let gen_folder = path.resolve(appDir, "generated_data");
let save = require("./save");
let public_data = path.resolve(__dirname, "..", "public", "data");

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'CHARTextract' });
});

router.get("/get_project_settings", function(req, res, next) {
    let jsonPromise = new Promise(function (resolve, reject) {
        fs.readFile(path.join(public_data, "project_settings.json"), 'utf8', function(err, data) {
            if (err){
                reject(err);
            }
            else {
                resolve(JSON.parse(data))
            }
        });
    });
    jsonPromise.then(function(result){
        if (result.hasOwnProperty("Rules Folder")) {
            save.rules_path = path.join(...result["Rules Folder"]);
            console.log("Settings Rules Path in index to " + save.rules_path)
        }
        else {
            save.rules_path = null;
        }
        res.send(JSON.stringify(result));
    });
});

router.get("/:variable/:dataset/error_report.json", function(req, res, next) {
    let reportPromise = new Promise(function (resolve, reject) {
        fs.readFile(path.join(gen_folder, req.params["variable"], req.params["dataset"],"error_report.json"), 'utf8', function(err, data) {
            if (err){
                reject(err);
            }
            else {
             resolve(JSON.parse(data))
            }
           });
    });
    reportPromise.then(function(result){
        res.send(JSON.stringify(result));
    });
    //var json = JSON.parse(fs.readFileSync(path.join("public", "data", "error_report.json")));
});

module.exports = router;
