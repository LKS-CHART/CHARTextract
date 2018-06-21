var express = require('express');
var router = express.Router();
var pyshell = require('../python_connector/connector');
var fs = require("fs");
var path = require("path");
var filePath = "./public/data/project_settings.json";

//let out_rules_path = "Z:\\LKS-CHART\\Projects\\NLP POC\\Study data\\TB\\dev\\rules\\tb_rules";
//let rules_path = "Z:\\GEMINI-SYNCOPE\\NLP Validation Project\\training\\fixed set\\Regexes";

router.post('/save_project_settings', function(req, res, next) {

    fs.writeFile(filePath, JSON.stringify(req.body["Project Settings Data"], null, 4), function(err) {

        if(err) {
            return console.log(err)
        }

        console.log("Save Settings")
        console.log(req.body)
        module.exports.rules_path = path.join(...req.body["Project Settings Data"]["Rules Folder"]);
        res.sendStatus(200);
    })

});

router.post('/save_variable_settings/:variable', function(req, res, next) {
    var variable = req.params.variable;
    var save_var_path = path.join(module.exports.rules_path, variable);
    if(fs.existsSync(save_var_path)) {
        fs.writeFile(path.join(save_var_path, "rule_properties.json"), JSON.stringify(req.body["Variable Settings"], null, 4), function(err) {
            if(err) {
                return console.log(err);
            }

            console.log("Save Variable Settings");
            res.sendStatus(200);

        })
    } else
    {
        fs.mkdirSync(save_var_path);
        fs.writeFile(path.join(save_var_path, "rule_properties.json"), JSON.stringify(req.body["Variable Settings"], null, 4), function(err) {
            if(err) {
                return console.log(err);
            }


            fs.writeFile(path.join(save_var_path, "rule_settings.json"), JSON.stringify({"Classifier Type": "RegexClassifier"}, null, 4), function(err) {
                if(err) {
                    return console.log(err);
                }

                fs.writeFile(path.join(save_var_path, "Yes.txt"), "!Yes\n#Change class name by editing line above", function(err) {

                    if(err) {
                        return console.log(err);
                    }
                    res.sendStatus(200);
                })
            })
        })
    }

})

router.post('/:variable/:class', function(req, res, next) {

    if (module.exports.rules_path === null) {
        console.log("No Rules Path Specified");
        res.sendStatus(404);
    }

    var filePath = path.join(module.exports.rules_path, req.params['variable'], req.body.filename);

    console.log("HERE")

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

module.exports = router;
module.exports.rules_path = null;
