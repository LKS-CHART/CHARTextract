app.service('RuleService', [function() {
    //List of uncompiled rules (called a Ruleset)
    var URules = []; 

    //Uncompiled dummy rule format
    var Udummy_rule = {"Primary": {"Rule": [], "CRule": "This is a primary rule", "Score": 0, "Selected": false, "type": "Primary"}, "Secondary": {"Replace": [], "Ignore": [], "Add": []}}
    var Udummy_secondary_rule = {"Rule": [], "CRule": "This is a secondary rule", "Score": 0, "Modifier": "None", "Selected": false}

    var CurrentRule = null;


    function generateId() {

        return Math.random().toString(36).substring(7);
    }

    var addDummyRule = function() {
        var dummyRule = angular.copy(Udummy_rule)
        dummyRule.Primary["u_id"] = generateId()
        URules.push(dummyRule);

        return dummyRule
    }

    var addDummySecondary = function(index, rule_type) {
        var dummySecondaryRule = angular.copy(Udummy_secondary_rule)
        dummySecondaryRule["u_id"] = generateId();
        URules[index]["Secondary"][rule_type].push(dummySecondaryRule);

        return dummySecondaryRule
    }


    var getRuleset = function() {
        return URules;
    }

    var getRule = function(index) {
        return URules[index];
    }

    var deleteRule = function(index) {
        URules.splice(index, 1);
    }

    var deleteSecondaryRule = function(index, secondary_index, rule_type) {
        URules[index]["Secondary"][rule_type].splice(secondary_index, 1);
    }

    var getCurrentRule = function() {
        return CurrentRule;
    }

    var setCurrentRule = function(curRule) {
        CurrentRule = curRule;
        console.log(CurrentRule)

        return CurrentRule;
    }

    return {
        addDummyRule: addDummyRule,
        getRuleset: getRuleset,
        getRule: getRule,
        deleteRule: deleteRule,
        addDummySecondary: addDummySecondary,
        deleteSecondaryRule: deleteSecondaryRule,
        getCurrentRule: getCurrentRule,
        setCurrentRule: setCurrentRule
    };

}])