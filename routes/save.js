var express = require('express');
var router = express.Router();
var pyshell = require('../python_connector/connector');

router.post('/:variable/:class', function(req, res, next) {
    pyshell.send({'function': 'save', 'params': req.params});
    console.log("Received save");
    console.log(req.params);
    console.log(req.body);
    res.sendStatus(200);
});

module.exports = router;
