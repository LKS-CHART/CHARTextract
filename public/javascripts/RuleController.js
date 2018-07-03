app.controller("RuleController", ["DataService", "$http", "SettingsService", "MainRuleService", "RuleService", "$scope", function(DataService, $http, SettingsService, MainRuleService, RuleService, $scope) {

    var ruleController = this;

    ruleController.previousTab = null;
    ruleController.currentTab = null;
    ruleController.currentVar = null;

    ruleController.currentVar = SettingsService.getCurrentVariable();

    ruleController.availableClasses = [];
    ruleController.advancedMode = true;

    function loadText() {
        var url = "http://localhost:3000/load/" + ruleController.currentVar;
        console.log(url)
        $http.get(url).then(function(response) {

            var data = response.data

            if (Object.keys(data).length > 0) {

                if (ruleController.currentTab === null) {
                    var first_key = Object.keys(data)[0]
                    editor.session.setValue(data[first_key]["regexesText"]);
                    ruleController.currentTab = first_key;

                    if (data[first_key].hasOwnProperty("regexesSimple")) {
                        RuleService.setRuleset(data[first_key]["regexesSimple"])
                        $scope.$broadcast("ruleSetUpdate",null)
                    }
                }

                ruleController.availableClasses = [];
                MainRuleService.clearRulesets();
                Object.keys(data).forEach(function(key, val) {
                    if (ruleController.availableClasses.indexOf(key) === -1 && key !== SettingsService.getCurrentNegativeLabel()) {
                        ruleController.availableClasses.push(key);
                        MainRuleService.addToRulesets(key, data[key])
                    }
                })
            }
        })
    }

    loadText();

    ruleController.loadFile = function(class_name) {
        ruleController.previousTab = angular.copy(ruleController.currentTab);
        ruleController.currentTab = class_name;
        MainRuleService.setRulesetParam(ruleController.previousTab, "regexesText", editor.session.getValue());
        MainRuleService.setRulesetParam(ruleController.previousTab, "regexesSimple", RuleService.getRuleset());
        editor.session.setValue(MainRuleService.getRulesetParam(ruleController.currentTab, "regexesText"));
        RuleService.setRuleset(MainRuleService.getRulesetParam(ruleController.currentTab, "regexesSimple"));
        $scope.$broadcast("ruleSetUpdate",null)

    }

    ruleController.getNegativeLabel = function() {
        return SettingsService.getCurrentNegativeLabel();
    }

    ruleController.deleteFile = function(class_name) {
        var url = "http://localhost:3000/delete/" + ruleController.currentVar + "/" + class_name;

        var params = {
            "filename": MainRuleService.getRulesetParam(class_name, "filename")
        }

        console.log(params)

        $http.post(url, params).then(function() {
            console.log("Deleted File")
            MainRuleService.deleteRuleset(class_name);
            var index = ruleController.availableClasses.indexOf(class_name)
            ruleController.availableClasses.splice(index,1);
            ruleController.previousTab = null;

            if (ruleController.availableClasses.length > 0) {
                var new_index = index === ruleController.availableClasses.length ? index - 1 : index;
                var new_class = ruleController.availableClasses[new_index];
                editor.session.setValue(MainRuleService.getRulesetParam(new_class, "regexesText"))
                RuleService.setRuleset(MainRuleService.getRulesetParam(new_class, "regexesSimple"));
                $scope.$broadcast("ruleSetUpdate",null)
                ruleController.currentTab = new_class
            }
        })
    }
    ruleController.saveFile = function(class_name) {

        var new_class_name = MainRuleService.getRulesetParam(class_name, "new_name") || class_name

        if (new_class_name !== SettingsService.getCurrentNegativeLabel()) {

            MainRuleService.setRulesetParam(class_name, "regexesText", editor.session.getValue());
            MainRuleService.setRulesetParam(class_name, "regexesSimple", RuleService.getRuleset());
            var url = "http://localhost:3000/save/" + ruleController.currentVar + "/" + new_class_name
            var params = {
                "filename": MainRuleService.getRulesetParam(class_name, "filename"),
                "regexes": MainRuleService.getRulesetParam(class_name, "regexesText"),
                "new_name": new_class_name,
                "regexesSimple": MainRuleService.getRulesetParam(class_name, "regexesSimple")
            }
            $http.post(url, params).then(function(data) {
                console.log("Sent Post Request")
            }).then(function() {
                ruleController.currentTab = new_class_name;
            })
        }

        loadText();
    }

    ruleController.createNewClass = function() {
        var temp_class_name = ruleController.availableClasses.length
        ruleController.availableClasses.push(temp_class_name);

        if (ruleController.previousTab !== null) {

            ruleController.previousTab = angular.copy(ruleController.currentTab);
        }
        ruleController.currentTab = temp_class_name

        var dummyRuleset = {
            "filename": temp_class_name + ".txt",
            "regexesText": "!" + temp_class_name + "\n#Don't forget to save the file to preserve the new name.",
            "new_name": null,
            "regexesSimple": []
        }
        MainRuleService.addToRulesets(temp_class_name, dummyRuleset)

        if (ruleController.previousTab !== null) {
            MainRuleService.setRulesetParam(ruleController.previousTab, "regexesText", editor.session.getValue());
            MainRuleService.setRulesetParam(ruleController.previousTab, "regexesSimple", RuleService.getRuleset());
        }

        editor.session.setValue(MainRuleService.getRulesetParam(temp_class_name, "regexesText"))
        RuleService.setRuleset(MainRuleService.getRulesetParam(temp_class_name, "regexesSimple"));
        $scope.$broadcast("ruleSetUpdate",null)

        var url = "http://localhost:3000/save/" + ruleController.currentVar + "/" + temp_class_name;

        var params = {
            "filename": MainRuleService.getRulesetParam(temp_class_name, "filename"),
            "regexes": MainRuleService.getRulesetParam(temp_class_name, "regexesText"),
            "new_name": null,
            "regexesSimple": MainRuleService.getRulesetParam(temp_class_name, "regexesSimple")
        }

        $http.post(url, params).then(function(data) {
            console.log("Sent Post Request")
        })
    }

    $(document).on("keyup", ".cspan", function(e) {
        var illegal_chars = new Set(["!", ";", ",", "\\", "/", "\"", "'", "#"])
        if(e.keyCode == 9 || illegal_chars.has(e.key)) {
            e.preventDefault();
        }

        editor.session.replace({start: {row: 0, column: 1},
                              end: {row: 0, column: Number.MAX_VALUE}}, $(this).text());

        MainRuleService.setRulesetParam(ruleController.currentTab, "new_name", $(this).text());
    });
}])