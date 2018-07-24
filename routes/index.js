let express = require('express');
let router = express.Router();
let fs = require('fs');
let path = require('path');
let baseDir = process.env[(process.platform === 'win32') ? 'USERPROFILE' : 'HOME'];
let gen_folder = path.resolve(__dirname, "..", "RegexNLP-py", "generated_data");
var save = require("./save");
var public_data = path.resolve(__dirname, "..", "public", "data");
/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.get("/get_project_settings", function(req, res, next) {
    var json = JSON.parse(fs.readFileSync(path.join(public_data, "project_settings.json")));
    console.log("IN GET PROJECT SETTINGS")
    if (json.hasOwnProperty("Rules Folder")) {
        save.rules_path = path.join(...json["Rules Folder"]);
        console.log("Settings Rules Path in index")
    }
    else {
        save.rules_path = null;
    }

    res.send(JSON.stringify(json));
});

router.get("/:variable/:dataset/error_report.json", function(req, res, next) {
    var reportPromise = new Promise(function (resolve, reject) {
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

router.get("error_report.json", function(req, res, next) {
    var json = JSON.parse(fs.readFileSync(path.join(public_data, "error_report.json")));
    res.send(JSON.stringify(json));
});
module.exports = router;
