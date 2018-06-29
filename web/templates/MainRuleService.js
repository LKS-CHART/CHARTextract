app.service("MainRuleService", ["RuleService", function(RuleService) {

    var allRulesets = {};

    var getRulesets = function() {
        return allRulesets;
    }

    var getRuleset = function(key) {
        return allRulesets[key];
    }

    var addToRulesets = function(class_name, ruleset) {
        allRulesets[class_name] = ruleset;
    }

    return {
        allRulesets: allRulesets,
        getRuleset: getRuleset,
        addToRulesets: addToRulesets
    }

}])