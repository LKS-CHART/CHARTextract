app.controller("RuleController", ["DataService", "$http", "SettingsService", "MainRuleService", "RuleService", "$scope", "$rootScope", "$q", function(DataService, $http, SettingsService, MainRuleService, RuleService, $scope, $rootScope, $q) {

    var ruleController = this;

    ruleController.previousTab = null;
    ruleController.currentTab = null;
    ruleController.currentVar = null;

    ruleController.currentVar = SettingsService.getCurrentVariable();

    ruleController.availableClasses = {};
    ruleController.advancedMode = false;

    $scope.$on("run_variable", function() {
        console.log("EVENT RUN VAR - RULECONTROLLER")
        ruleController.saveFile(ruleController.currentTab)

    })

    $scope.$on("$destroy", function() {
        $rootScope.$broadcast("ruleCtrl_despawn")

        if (ruleController.currentTab) {
            ruleController.saveFile(ruleController.currentTab)
        }
    })


    function generateId() {

        return Math.random().toString(36).substring(7);
    }

    function loadText() {
        var url = "/load/" + ruleController.currentVar;
        $http.get(url).then(function(response) {

            var data = response.data

            if (Object.keys(data).length > 0) {

                ruleController.availableClasses = {};
                MainRuleService.clearRulesets();
                Object.keys(data).forEach(function(key, val) {
                    ruleController.availableClasses[generateId()] = key;
                    MainRuleService.addToRulesets(key, data[key])
//                    if (ruleController.availableClasses.indexOf(key) === -1 && key !== SettingsService.getCurrentNegativeLabel()) {
//                    }
                })

                if (ruleController.currentTab === null) {
                    var first_tab = Object.keys(ruleController.availableClasses)[0]
                    var first_key = ruleController.availableClasses[first_tab]
                    ruleController.currentTab = first_tab
                    editor.session.setValue(data[first_key]["regexesText"]);

                    if (data[first_key].hasOwnProperty("regexesSimple")) {
                        RuleService.setRuleset(data[first_key]["regexesSimple"])
                        $scope.$broadcast("ruleSetUpdate",null)
                    }
                }
            }
        })
    }

    loadText();

    ruleController.loadFile = function(tab_name) {
        var prev_tab = angular.copy(ruleController.currentTab);
        console.log(prev_tab)
        ruleController.previousTab = prev_tab
        ruleController.currentTab = tab_name;

        var promise = ruleController.saveFile(prev_tab)

        promise.then(function() {
            editor.session.setValue(MainRuleService.getRulesetParam(ruleController.availableClasses[tab_name], "regexesText"));
            RuleService.setRuleset(MainRuleService.getRulesetParam(ruleController.availableClasses[tab_name], "regexesSimple"));
            $scope.$broadcast("ruleSetUpdate",null)
            console.log("LOADED class")
        })
    }

    ruleController.getNegativeLabel = function() {
        return SettingsService.getCurrentNegativeLabel();
    }

    ruleController.deleteFile = function(tab_name) {

        var class_name = ruleController.availableClasses[tab_name]
        var url = "/delete/" + ruleController.currentVar + "/" + class_name;

        var params = {
            "filename": MainRuleService.getRulesetParam(class_name, "filename")
        }

        console.log(params)

        $http.post(url, params).then(function() {
            console.log("Deleted File")
            MainRuleService.deleteRuleset(class_name);
            var availableClasses = Object.keys(ruleController.availableClasses)
            console.log(availableClasses)
            var index = availableClasses.indexOf(tab_name)

            delete ruleController.availableClasses[tab_name]
            availableClasses.splice(index,1);

            ruleController.previousTab = null;

            if (availableClasses.length > 0) {
                var new_index = index === availableClasses.length ? index - 1 : index;
                var new_tab = availableClasses[new_index];
                console.log(new_tab)
                var new_class = ruleController.availableClasses[new_tab]
                editor.session.setValue(MainRuleService.getRulesetParam(new_class, "regexesText"))
                RuleService.setRuleset(MainRuleService.getRulesetParam(new_class, "regexesSimple"));
                $scope.$broadcast("ruleSetUpdate",null)
                ruleController.currentTab = new_tab
            } else {
                ruleController.currentTab = null;
            }
        })
    }
    ruleController.saveFile = function(tab_name) {

        $rootScope.$broadcast("saving")
        var deferred = $q.defer();
        var class_name = ruleController.availableClasses[tab_name]
        var new_class_name = MainRuleService.getRulesetParam(class_name, "new_name") || class_name

        if (new_class_name !== SettingsService.getCurrentNegativeLabel()) {

            MainRuleService.setRulesetParam(class_name, "regexesText", editor.session.getValue());
            MainRuleService.setRulesetParam(class_name, "regexesSimple", RuleService.getRuleset());
            var url = "/save/" + ruleController.currentVar + "/" + new_class_name
            var params = {
                "filename": MainRuleService.getRulesetParam(class_name, "filename"),
                "regexes": MainRuleService.getRulesetParam(class_name, "regexesText"),
                "new_name": new_class_name,
                "Dirty": false,
                "regexesSimple": MainRuleService.getRulesetParam(class_name, "regexesSimple")
            }
            $http.post(url, params).then(function(data) {
                console.log("SAVED")
                $rootScope.$broadcast("save_finished")
            })

            deferred.resolve();
        }

        return deferred.promise;
//        loadText();
    }

    ruleController.createNewClass = function() {
        var temp_class_name = Object.keys(ruleController.availableClasses).length
        var new_tab_id = generateId()
        ruleController.availableClasses[new_tab_id] = temp_class_name;

        if (ruleController.currentTab !== null) {
            ruleController.previousTab = angular.copy(ruleController.currentTab);
        }
        ruleController.currentTab = new_tab_id

        var dummyRuleset = {
            "filename": temp_class_name + ".txt",
            "regexesText": "!" + temp_class_name + "\n#Don't forget to save the file to preserve the new name.",
            "new_name": null,
            "regexesSimple": []
        }
        MainRuleService.addToRulesets(temp_class_name, dummyRuleset)

        console.log(ruleController.previousTab)
        if (ruleController.previousTab === null) {
            editor.session.setValue(MainRuleService.getRulesetParam(temp_class_name, "regexesText"))
            RuleService.setRuleset(MainRuleService.getRulesetParam(temp_class_name, "regexesSimple"));
            $scope.$broadcast("ruleSetUpdate",null)
        } else {
            console.log("ASDDASD")
            var promise = ruleController.saveFile(ruleController.previousTab)
            promise.then(function() {
                editor.session.setValue(MainRuleService.getRulesetParam(temp_class_name, "regexesText"))
                RuleService.setRuleset(MainRuleService.getRulesetParam(temp_class_name, "regexesSimple"));
                $scope.$broadcast("ruleSetUpdate",null)
                console.log("SAVED PREVIOUS ON CREATION")
            })
        }

        var url = "/save/" + ruleController.currentVar + "/" + temp_class_name;

        var params = {
            "filename": temp_class_name + ".txt",
            "regexes": "!" + temp_class_name + "\n#Don't forget to save the file to preserve the new name.",
            "new_name": null,
            "regexesSimple": []
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


        MainRuleService.setRulesetParam(ruleController.availableClasses[ruleController.currentTab], "new_name",
                                                                                                        $(this).text());
    });

    $rootScope.$broadcast("ruleCtrl_spawn")
}])