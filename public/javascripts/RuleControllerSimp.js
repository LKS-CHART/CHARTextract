//Controls the addition and manipulation of Rules
app.controller("RuleControllerSimp", ["RuleService", "$scope", function(RuleService, $scope){
    /*

        MainRuleService:

        list of all rules for all classes. Indexed by class name. Raw text and structured ones from RcSimp.
        Can reference and index by class name.

        Have reference to RuleService in RuleController.
        Set RuleSet on tab swap, save and create
    */
    var rc = this;
    console.log("IN RuleControllerSimp")
    rc.test = "This is a test";
    rc.rules = RuleService.getRuleset();
    rc.selectedRuleObject = "alskdjalskdjaslkdj";
    rc.selectedRule = RuleService.getCurrentRule();

    //Adds a dummy rule to the Ruleset 
    rc.addRule = function() {
       rc.selectRule(RuleService.addDummyRule().Primary);
    }

    $scope.$on("ruleSetUpdate", function(event, data) {
        rc.rules = RuleService.getRuleset();
    })

    rc.getCurrentRule = function() {
        return RuleService.getCurrentRule();
    }

    rc.addSecondaryRule = function(rule, ruleType, $event) {
        var index = rc.rules.indexOf(rule);
        rc.selectRule(RuleService.addDummySecondary(index, ruleType))
        $event.stopPropagation();
    }

    rc.deletePrimary = function(rule) {
        var index = rc.rules.indexOf(rule);
        RuleService.deleteRule(index);
    }

    rc.clearSelected = function() {

        angular.forEach(rc.rules, function(value, key) {
            value.Primary.Selected = false;
            
            angular.forEach(value.Secondary, function(svalue, skey) {
                angular.forEach(svalue, function(rvalue, rkey) {
                    rvalue.Selected = false;
                })
            })
        })
    }

    rc.deleteSecondary = function(rule, secondary_rule, rule_type) {
        var index_rule = rc.rules.indexOf(rule);
        var index_secondary = rule["Secondary"][rule_type].indexOf(secondary_rule);
        RuleService.deleteSecondaryRule(index_rule, index_secondary, rule_type)
    }

    rc.selectRule = function(rule) {
        rc.selectedRule = RuleService.setCurrentRule(rule);
        rc.clearSelected();

        rc.selectedRule.Selected = true;
        console.log(rc.selectedRule)
    }

}])