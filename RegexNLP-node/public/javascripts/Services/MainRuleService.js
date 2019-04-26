app.service("MainRuleService", ["RuleService", function(RuleService) {

    console.log("MAIN RULE SERVICE LOADED")
    var allRulesets = {};
    var currentMode = "simple";

    var setMode = function(mode) {
        currentMode = mode;
    }

    var getMode = function() {
        return currentMode;
    }

    var getRulesets = function() {
        return allRulesets;
    }

    var getRuleset = function(key) {
        return allRulesets[key];
    }

    var addToRulesets = function(class_name, ruleset) {
        allRulesets[class_name] = ruleset;
    }

    var clearRulesets = function() {
        allRulesets = {};
    }

    var setRuleset = function(class_name, new_ruleset) {
        allRulesets[class_name] = new_ruleset;
    }

    var setRulesetParam = function(class_name, param, value) {
        allRulesets[class_name][param] = value;
    }
    var getRulesetParam = function(class_name, param) {
        return allRulesets[class_name][param];
    }

    var deleteRuleset = function(class_name) {
        delete allRulesets[class_name];
    }

    return {
        getRulesets: getRulesets,
        getRuleset: getRuleset,
        addToRulesets: addToRulesets,
        setRuleset: setRuleset,
        clearRulesets: clearRulesets,
        setRulesetParam: setRulesetParam,
        getRulesetParam: getRulesetParam,
        deleteRuleset: deleteRuleset,
        setMode: setMode,
        getMode: getMode
    }

}])