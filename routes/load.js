let express = require('express');
let router = express.Router();
let rules_path = "Z:\\LKS-CHART\\Projects\\NLP POC\\Study data\\TB\\dev\\rules\\tb_rules";
//rules_path = "Z:\\GEMINI-SYNCOPE\\NLP Validation Project\\training\\fixed set\\Regexes";
let fs = require('fs');
let path = require('path');

router.get('/:variable', function(req, res, next) {
    console.log("Received load");
    dataJSON = {};
    filePath = path.join(rules_path, req.params['variable']);

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
