let express = require('express');
let router = express.Router();
let fs = require('fs');
let path = require('path');
const os = require('os');
let winDrives = require('../path_helper/win-drives');

function promisify(fn) {
    /**
     * @param {...Any} params The params to pass into *fn*
     * @return {Promise<Any|Any[]>}
     */
    return function promisified(...params) {
        return new Promise((resolve, reject) => fn(...params.concat([(err, ...args) => err ? reject(err) : resolve( args.length < 2 ? args[0] : args )])))
    }
}

/* GET home page. */
function get_directory(tokenized_path){
    cur_path = path.normalize(path.join(...tokenized_path.slice(1)));
    console.log(tokenized_path.slice(1));
    if (tokenized_path.length === 1){
        let childDirs = winDrives.usedLetters();
        return childDirs.then(function (result){
            let arr = [];
            result.forEach(file_name => {
                 arr.push({
                     "filename": file_name,
                     "Root": ["Computer"],
                     "filepath": ["Computer", file_name + "\\"],
                     "Type": "Folder",
                     "Children": []
                 });
            });
            return arr;
        }).catch(function(error){
            console.log("Error reading " + cur_path + " : " + error);
            return "Error reading " + cur_path + " : " + error;
        })
    } else {
        if (!fs.statSync(cur_path).isDirectory()){
            return [];
        }
        let childDirs = promisify(fs.readdir);
        return childDirs(cur_path).then(function (result){
            let arr = [];
            result.forEach(file_name => {
                try {
                arr.push({
                    "filename": file_name,
                    "Root": tokenized_path,
                    "filepath": tokenized_path.concat([file_name]),
                    "Type": fs.statSync(path.join(cur_path, file_name)).isDirectory() ? "Folder" : "File",
                    "Children": []
                });} catch(err) {
                    console.log(err);
                }
            });
            return arr;
        }).catch(function(error){
            console.log("Error reading " + cur_path + " : " + error);
            return "Error reading " + cur_path + " : " + error;
        })
    }
}

// let arr = [];
// console.log(path.normalize(path.join("C:")));
// x = get_directory(["Computer", "C:\\"]);
// x.then(function (result){ console.log(result)});
//get_directory(["Computer","Z:","GEMINI-SYNCOPE"]);
router.post('/', function(req, res, next) {
    console.log(req.body["path"]);
    if (req.body["path"].length === 1){
        let res_json = {
            "filename": req.body["path"][req.body["path"].length - 1],
            "Root": [],
            "filepath": ["Computer"],
            "Type": "Folder"
        };
        let cur_promise = new Promise(function (resolve, reject) {
            resolve(get_directory(req.body["path"]))});
        cur_promise.then(function(result){
            res_json["Children"] = result;
            res.send(JSON.stringify(res_json));
        });
    } else {
        cur_path = path.normalize(path.join(...req.body["path"].slice(1)));
        console.log(cur_path);
        let res_json = {
            "filename": req.body["path"][req.body["path"].length - 1],
            "Root": req.body["path"].slice(req.body["path"].length - 1),
            "filepath": req.body["path"],
            "Type": fs.statSync(path.join(cur_path)).isDirectory() ? "Folder" : "File",
        };
        let cur_promise = new Promise(function (resolve, reject) {
            resolve(get_directory(req.body["path"]))});
        cur_promise.then(function(result){
            res_json["Children"] = result;
            res.send(JSON.stringify(res_json));
        });
    }

});


router.get('/', function(req, res, next) {
    let res_json = {
        "filename": "Computer",
        "Root": [],
        "filepath": ["Computer"],
        "Type": "Folder"
    };
    let cur_promise = new Promise(function (resolve, reject) {
        resolve(get_directory(["Computer"]));
    });
    cur_promise.then(function(result){
        res_json["Children"] = result;
        res.send(JSON.stringify(res_json));
    });
});

module.exports = router;
