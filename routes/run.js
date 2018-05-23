var express = require('express');
var router = express.Router();


/* Save resource as json */
router.get('/:variable/:class', function(req, res, next) {
    pyshell.send({'function': 'run', 'params': req.params});
    console.log(req.toString());
    console.log(req.params);
    res.send(req.params);
});

module.exports = router;
