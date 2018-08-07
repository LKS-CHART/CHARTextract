let express = require('express');
let router = express.Router();
let fs = require('fs');
let path = require('path');
//let baseDir = process.env[(process.platform === 'win32') ? 'USERPROFILE' : 'HOME'];
let appDir = require('../path_helper/paths').getAppRoot();
let gen_folder = path.resolve(appDir, "generated_data");

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'RegexNLP' });
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
});

module.exports = router;