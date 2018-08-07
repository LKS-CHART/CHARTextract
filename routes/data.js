let express = require('express');
let save = require('./save');
let router = express.Router();
//let rules_path = "Z:\\LKS-CHART\\Projects\\NLP POC\\Study data\\TB\\dev\\rules\\tb_rules";
//rules_path = "Z:\\GEMINI-SYNCOPE\\NLP Validation Project\\training\\fixed set\\Regexes";
let fs = require('fs');
let path = require('path');
let public_path = path.resolve("public", "data");
let default_path = path.resolve("defaults");

function promisify(fn) {
    /**
     * @param {...Any} params The params to pass into *fn*
     * @return {Promise<Any|Any[]>}
     */
    return function promisified(...params) {
        return new Promise((resolve, reject) => fn(...params.concat([(err, ...args) => err ? reject(err) : resolve( args.length < 2 ? args[0] : args )])))
    }
}

router.get('/default_variable_settings', function(req, res, next) {
    let variable_properties = path.join(default_path, "rule_properties.json");
    let fR = promisify(fs.readFile);

    fR(variable_properties).then(data => {
        let res_json = JSON.parse(data);
        console.log(res_json);
        res.send(JSON.stringify(res_json));

    })
});

router.get('/error_report.json', function(req, res, next) {
    console.log("WE IS HERE");

    let fR = promisify(fs.readFile);

    fR(path.join(public_path, "error_report.json"), "utf-8").then(data => {
        let res_json = JSON.parse(data);
        res.send(JSON.stringify(res_json))
    }).catch( err => {
        fR(path.join(default_path, "error_report.json"), "utf-8").then(data => {
            let res_json = JSON.parse(data);
            res.send(JSON.stringify(res_json))
        }).catch( err => {
            console.log(err);
        })}
    );
});

function changeRulesPath(result){
    if (result.hasOwnProperty("Rules Folder")) {
        save.rules_path = path.join(...result["Rules Folder"]);
        console.log("Settings Rules Path in index to " + save.rules_path)
    }
    else {
        console.log("Rules Path not set");
        save.rules_path = null;
    }
}

let getProjectSettings =
    new Promise(function(resolve, reject){
        let fileReq = promisify(fs.readFile);
        fileReq(path.join(public_path, "project_settings.json"), "utf-8").then(data => {
            let res_json = JSON.parse(data);
            changeRulesPath(res_json);
            resolve(JSON.stringify(res_json));
        }).catch(err => {
                fileReq(path.join(default_path, "project_settings.json"), "utf-8").then(data => {
                    let res_json = JSON.parse(data);
                    changeRulesPath(res_json);
                    resolve(JSON.stringify(res_json));
                }).catch(err => {
                    reject(err);
                })
            }
        );
    });

router.get('/project_settings.json', function(req, res, next) {
    getProjectSettings.then(function(result){
        res.send(result);
    }).catch(function(err){
        console.log(err);
        res.sendStatus(404);
    })
});

getProjectSettings.then(function(result) {
    console.log(result);
    console.log("Running Project Settings once");
});

module.exports = router;
