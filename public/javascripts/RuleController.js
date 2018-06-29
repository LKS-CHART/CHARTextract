app.controller("RuleController", ["DataService", "$http", "SettingsService", "MainRuleService", function(DataService, $http, SettingsService, MainRuleService) {

    var ruleController = this;

    ruleController.ruleData = {};
    ruleController.previousTab = null;
    ruleController.currentTab = null;
    ruleController.currentVar = null;

    ruleController.currentVar = SettingsService.getCurrentVariable();

    ruleController.availableVars = [];
    ruleController.advancedMode = true;

    function loadText() {
        var url = "http://localhost:3000/load/" + ruleController.currentVar;
        console.log(url)
        $http.get(url).then(function(response) {
            ruleController.ruleData = response.data
            console.log(ruleController.ruleData)

            if (Object.keys(ruleController.ruleData).length > 0) {

                if (ruleController.currentTab === null) {
                    var first_key = Object.keys(ruleController.ruleData)[0]
                    editor.session.setValue(ruleController.ruleData[first_key]["regexesText"]);
                    ruleController.currentTab = first_key;
                }

                ruleController.availableVars = [];
                Object.keys(ruleController.ruleData).forEach(function(key, val) {
                    if (ruleController.availableVars.indexOf(key) === -1) {
                        ruleController.availableVars.push(key);
                    }
                })
            }
        })
    }

    loadText();

    ruleController.loadFile = function(class_name) {
        ruleController.previousTab = angular.copy(ruleController.currentTab);
        ruleController.currentTab = class_name;
        ruleController.ruleData[ruleController.previousTab]["regexesText"] = editor.session.getValue();
        editor.session.setValue(ruleController.ruleData[ruleController.currentTab]["regexesText"])

    }

    ruleController.getNegativeLabel = function() {
        return SettingsService.getCurrentNegativeLabel();
    }

    ruleController.deleteFile = function() {

    }
    ruleController.saveFile = function(class_name) {

        var new_class_name = ruleController.ruleData[class_name].new_name || class_name

        if (new_class_name !== SettingsService.getCurrentNegativeLabel()) {

            ruleController.ruleData[class_name]["regexesText"] = editor.session.getValue();
            var url = "http://localhost:3000/save/" + ruleController.currentVar + "/" + new_class_name
            var params = {
                "filename": ruleController.ruleData[class_name].fileName,
                "regexes": ruleController.ruleData[class_name].regexesText,
                "new_name": new_class_name
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
        var temp_class_name = ruleController.availableVars.length
        ruleController.availableVars.push(ruleController.availableVars.length);

        if (ruleController.previousTab !== null) {

            ruleController.previousTab = angular.copy(ruleController.currentTab);
        }
        ruleController.currentTab = temp_class_name
        ruleController.ruleData[temp_class_name] = {
            "fileName": temp_class_name + ".txt",
            "regexesText": "!" + temp_class_name + "\n#Don't forget to save the file to preserve the new name.",
            "new_name": null
        }

        if (ruleController.previousTab !== null) {
            ruleController.ruleData[ruleController.previousTab]["regexesText"] = editor.session.getValue();
        }

        editor.session.setValue(ruleController.ruleData[temp_class_name].regexesText)

        var url = "http://localhost:3000/save/" + ruleController.currentVar + "/" + temp_class_name;
        var params = {
            "filename": ruleController.ruleData[temp_class_name].fileName,
            "regexes": ruleController.ruleData[temp_class_name].regexesText,
            "new_name": null
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

        ruleController.ruleData[ruleController.currentTab]["new_name"] = $(this).text();


    });
}])