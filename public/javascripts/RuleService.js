app.service('RuleService', [function() {
    //List of uncompiled rules (called a Ruleset)
    var URules = []; 

    //Uncompiled dummy rule format
    var Udummy_rule = {"Primary": {"Rule": [], "Score": 0, "Selected": false, "type": "Primary"}, "Secondary": {"Replace": [], "Ignore": [], "Add": []}}
    var Udummy_secondary_rule = {"Rule": [],  "Score": 0, "Modifier": "None", "Selected": false}

    var CurrentRule = null;

    var cached_id = null;

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

    var setRuleset = function(new_ruleset) {
        URules = new_ruleset;
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

    var setCurrentRuleVals = function(vals) {
        CurrentRule["Rule"] = vals;
    }

    var getRuleById = function(id) {
        if (CurrentRule === null || CurrentRule.u_id !== id) {

            for(var rule_index = 0; rule_index < URules.length; rule_index++) {
                var primary_rule = URules[rule_index]["Primary"]

                if (primary_rule.u_id === id) {
                    CurrentRule = primary_rule
                    return CurrentRule
                }

                Object.keys(URules[rule_index]["Secondary"]).forEach(function(secType) {

                    for (var sec_rule_index = 0; sec_rule_index < URules[rule_index]["Secondary"][secType].length; sec_rule_index++) {
                        var secondary_rule = URules[rule_index]["Secondary"][secType][sec_rule_index]

                        if (secondary_rule.u_id === id) {
                            CurrentRule = secondary_rule;
                            return CurrentRule
                        }

                    }

                })


            }

        }

        else {
            return CurrentRule;

        }
    }

    return {
        addDummyRule: addDummyRule,
        getRuleset: getRuleset,
        getRule: getRule,
        deleteRule: deleteRule,
        addDummySecondary: addDummySecondary,
        deleteSecondaryRule: deleteSecondaryRule,
        getCurrentRule: getCurrentRule,
        setCurrentRule: setCurrentRule,
        setRuleset: setRuleset,
        getRuleById: getRuleById,
        setCurrentRuleVals: setCurrentRuleVals
    };

}])