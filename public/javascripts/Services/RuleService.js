app.service('RuleService', [function() {
    //List of uncompiled rules (called a Ruleset)
    console.log("RULESERVICE LOADED")
    var URules = [];
    let secondary_types = ["Replace", "Ignore", "Add"]

    //Uncompiled dummy rule format
    var Udummy_rule = {"Primary": {"Rule": [], "Score": 0, "Selected": false, "type": "Primary"}, "Secondary": {"Replace": [], "Ignore": [], "Add": []}}
    var Udummy_secondary_rule = {"Rule": [],  "Score": 0, "Modifier": "None", "Selected": false, "type": "None"}

    var CurrentRule = null;

    var QueriedRule = null;
    var QueriedContainer = null;
    var CachedJson = null;

    var cached_id = null;

    function generateId() {

        return Math.random().toString(36).substring(7);
    }

    var addPrimaryRule = function(rule) {
        var rule_copy = angular.copy(rule)
        rule_copy.Primary.Selected = false
        rule_copy.Primary["u_id"] = generateId()

        for (var k = 0; k < secondary_types.length; k++) {
            var secType = secondary_types[k]
            for (var sec_rule_index = 0; sec_rule_index < rule_copy["Secondary"][secType].length; sec_rule_index++) {
                var secondary_rule = rule_copy["Secondary"][secType][sec_rule_index]
                secondary_rule["u_id"] = generateId()
            }
        }

        URules.push(rule_copy)
    }

    var addSecondaryRule = function(index, rule_type, rule) {

        var rule_copy = angular.copy(rule)
        rule_copy.Selected = false
        rule_copy["u_id"] = generateId()

        URules[index]["Secondary"][rule_type].push(rule_copy)

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
        dummySecondaryRule["type"] = rule_type;
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

        return CurrentRule;
    }

    var setCurrentRuleVals = function(vals) {
        CurrentRule["Rule"] = vals;
    }

    var getRuleById = function(id) {

        if (QueriedRule === null || QueriedRule.u_id !== id) {

            for(var rule_index = 0; rule_index < URules.length; rule_index++) {
                var primary_rule = URules[rule_index]["Primary"]
                QueriedContainer = URules[rule_index]

                if (primary_rule.u_id === id) {
                    QueriedRule = primary_rule
                    CachedJson = {"Rule": QueriedRule, "Container": QueriedContainer, "index": rule_index}
                    return CachedJson
                }

                for (var k = 0; k < secondary_types.length; k++) {
                    var secType = secondary_types[k]
                    for (var sec_rule_index = 0; sec_rule_index < URules[rule_index]["Secondary"][secType].length; sec_rule_index++) {
                        var secondary_rule = URules[rule_index]["Secondary"][secType][sec_rule_index]

                        if (secondary_rule.u_id === id) {
                            QueriedRule = secondary_rule
                            QueriedContainer = secondary_rule
                            CachedJson = {"Rule": QueriedRule, "Container": QueriedContainer, "index": rule_index}
                            return CachedJson
                        }

                    }
                }

            }

        }

        else {
            return CachedJson

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
        setCurrentRuleVals: setCurrentRuleVals,
        addPrimaryRule: addPrimaryRule,
        addSecondaryRule: addSecondaryRule
    };

}])