let express = require('express');
let router = express.Router();
let pyshell = require('../python_connector/connector');
let rules_path = "Z:\\LKS-CHART\\Projects\\NLP POC\\Study data\\TB\\dev\\rules\\tb_rules";
let fs = require('fs');
let path = require('path');


router.get('/:variable', function(req, res, next) {
    console.log("Received load");
    dataJSON = {};
    filePath = path.join(rules_path, req.params['variable']);

    function appendData(fileName, resolve, reject){
        if (path.extname(fileName) === ".txt") {
            console.log(fileName);
            fs.readFile(path.join(filePath,fileName), {encoding: 'utf-8'}, function(err,data){
                if (!err) {
                    dataJSON[data.split(/[,\n\r]+/,2)[0].substring(1)] = {"fileName": fileName, "regexesText": data};
                    resolve(data);
                } else {
                    reject(err);
                    console.log(err);
                    res.sendStatus(404);
                }
            });
        }
        return dataJSON;
    }

    function sendData(){
        // console.log(dataJSON);
        res.setHeader('Access-Control-Allow-Origin', 'http://localhost:8080');
        res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');
        res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With, content-type')
        res.setHeader('Access-Control-Allow-Credentials', true);
        res.setHeader('Content-Type', 'application/json');
        res.send(JSON.stringify(dataJSON));
    }

    fs.readdir(filePath,{encoding: 'utf-8'}, function(err, files){
        if (!err){
            console.log(files);

            let getFiles = files.map((item) => {
                return new Promise((resolve, reject) => {
                    appendData(item, resolve, reject);
                })
            });
            Promise.all(getFiles).then(() => sendData());
        } else {
            console.log(err);
            res.sendStatus(404);
        }
    });


});

module.exports = router;
