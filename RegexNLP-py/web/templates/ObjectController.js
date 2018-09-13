app.controller("ObjectController", ["RuleService", "$rootScope", function(RuleService, $rootScope) {
    var oc = this;

    oc.rules = RuleService.getRuleset();
    oc.addObject = function(ruleObjectType) {
        oc.selectedRule = null;
        oc.selectedRule = RuleService.getCurrentRule();
        if (oc.selectedRule.Selected === true ) {

            var ruleObj = new classesMapping[ruleObjectType]();
            $rootScope.$broadcast("reloadTags", {"rule": oc.selectedRule, "text": ruleObj.text})

        }

    }
}])