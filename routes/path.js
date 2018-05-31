let express = require('express');
let router = express.Router();
let fs = require('fs');
let path = require('path');
let baseDir = process.env[(process.platform === 'win32') ? 'USERPROFILE' : 'HOME'];

/* GET home page. */
router.post('/', function(req, res, next) {
    res_json = { "filename": "Current Folder",
                "Root": "Full\\Path\\to\\Folder",
                "Type": "Folder",
                "Children": [
                    {
                        "filename": "Child of Current Folder",
                        "Root": "Full Path to Child of Current Folder",
                        "Type": "File",
                        "Children": []
                    }

                ]};
    res.render('index', { title: 'Express' });
});