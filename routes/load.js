let express = require('express');
let save = require('./save');
let router = express.Router();
//let rules_path = "Z:\\LKS-CHART\\Projects\\NLP POC\\Study data\\TB\\dev\\rules\\tb_rules";
//rules_path = "Z:\\GEMINI-SYNCOPE\\NLP Validation Project\\training\\fixed set\\Regexes";
let fs = require('fs');
let path = require('path');

function promisify(fn) {
    /**
     * @param {...Any} params The params to pass into *fn*
     * @return {Promise<Any|Any[]>}
     */
    return function promisified(...params) {
        return new Promise((resolve, reject) => fn(...params.concat([(err, ...args) => err ? reject(err) : resolve( args.length < 2 ? args[0] : args )])))
    }
}

function get_directory(rules_path){
    if (!fs.statSync(rules_path).isDirectory()){
        return [];
    }

    var count = 0;

    let childDirs = promisify(fs.readdir);
    return childDirs(rules_path).then(function (result){
        let arr = [];
        result.forEach(file_name => {
            try {
                if (fs.statSync(path.join(rules_path, file_name)).isDirectory()) {
                    arr.push({
                        "id": count,
                        "filename": file_name,
                    });

                    count++;
                }
            } catch(err) {
                console.log(err);
            }
        });
        return arr;
    }).catch(function(error){
        console.log("Error reading " + rules_path + " : " + error);
        return "Error reading " + rules_path + " : " + error;
    })
}

router.get('/variable_settings/:variable', function(req, res, next) {

    var variable_filePath = path.join(save.rules_path,req.params.variable)

    var variable_properties = path.join(variable_filePath, "rule_properties.json")

    var fR = promisify(fs.readFile)

    fR(variable_properties).then(data => {
        var res_json = JSON.parse(data);
        console.log(res_json)
        res.send(JSON.stringify(res_json))

    })

})

router.get('/classifier_settings/:variable', function(req, res, next) {
    var variable_filePath = path.join(save.rules_path, req.params.variable)
    var classifier_settings = path.join(variable_filePath, "rule_settings.json")

    var fR = promisify(fs.readFile)

    fR(classifier_settings).then(data => {
        var res_json = JSON.parse(data);
        res.send(JSON.stringify(res_json))
    })

})

router.get('/variable_list', function(req, res, next) {
    let res_json = {}

    if (save.rules_path === null) {
        console.log("Empty Rules Path");
        res.sendStatus(404);
        return;
    }

    let cur_promise = new Promise(function (resolve, reject) {
        console.log(save.rules_path)
        resolve(get_directory(save.rules_path))});

    cur_promise.then(function(result){
        res_json["Variable List"] = result;
        res.send(JSON.stringify(res_json));
    });
})
router.get('/:variable', function(req, res, next) {
    console.log("Received load");
    filePath = path.join(save.rules_path, req.params['variable']);
    dataJSON = {};

    console.log(filePath);

    function appendData(fileName, resolve, reject){
        if (path.extname(fileName) === ".txt") {
            console.log(fileName);
            fs.readFile(path.join(filePath,fileName), {encoding: 'utf-8'}, function(err, data){
                if (!err) {
                    dataJSON[data.split(/[,\n\r]+/,2)[0].substring(1)] = {"fileName": fileName, "regexesText": data};
                    resolve([fileName, data]);
                } else {
                    reject(err);
                    res.sendStatus(404);
                }
            });
        } else {
            reject("Not a file");
        }
        return dataJSON;
    }

    function sendData(result){
        res.send(JSON.stringify(dataJSON));
    }

    fs.readdir(filePath,{encoding: 'utf-8'}, function(err, files){
        if (!err){
            console.log(files);
            let final_promises = [];
            let getFiles = files.map((item) => {
                return new Promise((resolve, reject) => {
                    appendData(item, resolve, reject);
                }).catch((error) => {
                    console.log(error);
                })
            });
            //
            console.log(getFiles);
            // console.log(final_promises);
            Promise.all(getFiles).then(result => sendData(result));

        } else {
            console.log(err);
            res.sendStatus(404);
        }
    });


});

module.exports = router;
