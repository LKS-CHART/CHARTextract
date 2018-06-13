let express = require('express');
let router = express.Router();
let fs = require('fs');
let path = require('path');
let baseDir = process.env[(process.platform === 'win32') ? 'USERPROFILE' : 'HOME'];

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.get("/get_project_settings", function(req, res, next) {
    var json = JSON.parse(fs.readFileSync(path.join("public", "data", "project_settings.json")));
    res.send(JSON.stringify(json));
})

module.exports = router;
