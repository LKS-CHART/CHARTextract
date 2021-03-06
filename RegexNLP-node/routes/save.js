var express = require('express');
var router = express.Router();
var fs = require("fs");
var path = require("path");
var filePath = path.resolve(__dirname, "..", "public", "data", "project_settings.json");

router.post('/save_project_settings', function(req, res, next) {
    var project_settings = req.body["Project Settings Data"]
    
    fs.writeFile(filePath, JSON.stringify(project_settings, null, 4), function(err) {

        if(err) {
            return console.log(err)
        }

        console.log("Save Settings");
        console.log(req.body);
        module.exports.rules_path = path.join(...req.body["Project Settings Data"]["Rules Folder"]);
        res.sendStatus(200);
    })

});

router.post('/save_variable_settings/:variable', function(req, res, next) {
    var cur_variable = req.params['variable'];
    var save_var_path = path.join(module.exports.rules_path, cur_variable);
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

                fs.writeFile(path.join(save_var_path, "Yes.txt"), "!Yes\n#Don't forget to save the file to preserve the new name.", function(err) {
                    
                    if(err) {
                        return console.log(err);
                    }
                    res.sendStatus(200);
                })

                var new_json = {"Name": "Yes", "Dirty": false, "Rules": []};
                fs.writeFile(path.join(save_var_path, "Yes.json"), JSON.stringify(new_json, null, 4), function(err) {
                    if(err) {
                        return err
                    }
                })            
            })
        })
    }

});

router.post('/save_classifier_settings/:variable', function(req, res, next) {
    var cur_variable = req.params['variable'];
    var save_var_path = path.join(module.exports.rules_path, cur_variable);
    if(fs.existsSync(save_var_path)) {
        fs.writeFile(path.join(save_var_path, "rule_settings.json"), JSON.stringify(req.body["Classifier Settings"], null, 4), function(err) {
            if(err) {
                return console.log(err);
            }

            console.log("Save Classifier Settings");
            res.sendStatus(200);

        })
    }
});

router.post('/:variable/:class', function(req, res, next) {

    if (module.exports.rules_path === null) {
        console.log("No Rules Path Specified");
        res.sendStatus(404);
    }

    var filePath = path.join(module.exports.rules_path, req.params['variable'], req.body.filename);

    var index = filePath.indexOf(".txt");
    var jsonFilePath = filePath.substring(0,index) + ".json";
    var name = req.body.regexes.split(/[,\n\r]+/,2)[0].substring(1)
    fs.writeFile(filePath, req.body.regexes, function(err) {
        if(err) {
            return err;
        }
    });


    var new_json = {"Name": name, "Dirty": false, "Rules": req.body.regexesSimple};
    fs.writeFile(jsonFilePath, JSON.stringify(new_json, null, 4), function(err) {
        if(err) {
            return err
        }
    })

//    fs.writeFile(jsonFilePath, JSON.stringify(req.body.reg))
    console.log("Received save");
    console.log(req.params);
    console.log(req.body);
    res.sendStatus(200);
});

module.exports = router;
module.exports.rules_path = null;
