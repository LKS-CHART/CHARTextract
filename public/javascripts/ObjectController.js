app.controller("ObjectController", ["RuleService", function(RuleService) {
    var oc = this;

    oc.rules = RuleService.getRuleset();
    oc.addObject = function(ruleObjectType) {
        oc.selectedRule = null;
        oc.selectedRule = RuleService.getCurrentRule();
        if (oc.selectedRule.Selected === true ) {

            var ruleObj = new classesMapping[ruleObjectType]();
            
            oc.selectedRule.Rule.push(angular.copy(ruleObj))
        }

    }
}])