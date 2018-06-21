app.controller("RuleController", ["DataService", "$http", "SettingsService", function(DataService, $http, SettingsService) {

    var ruleController = this;
    var dataPromise = DataService.getData();

    ruleController.ruleData = null;
    ruleController.previousTab = null;
    ruleController.currentTab = null;
    ruleController.currentVar = null;

    ruleController.currentVar = SettingsService.getCurrentVariable();

    function loadText() {
        var url = "http://localhost:3000/load/" + ruleController.currentVar;
        console.log(url)
        $http.get(url).then(function(response) {
            ruleController.ruleData = response.data
            console.log(ruleController.ruleData)
            var first_key = Object.keys(ruleController.ruleData)[0]
            editor.session.setValue(ruleController.ruleData[first_key]["regexesText"]);
            ruleController.currentTab = first_key;
        })
    }

    loadText();

    ruleController.loadFile = function(class_name) {
        ruleController.previousTab = angular.copy(ruleController.currentTab);
        ruleController.currentTab = class_name;
        ruleController.ruleData[ruleController.previousTab]["regexesText"] = editor.session.getValue();
        editor.session.setValue(ruleController.ruleData[ruleController.currentTab]["regexesText"])

    }

    ruleController.saveFile = function(class_name) {
        ruleController.ruleData[class_name]["regexesText"] = editor.session.getValue();
        var url = "http://localhost:3000/save/" + ruleController.currentVar + "/" + ruleController.currentTab
        var params = {
            "filename": ruleController.ruleData[class_name].fileName,
            "regexes": ruleController.ruleData[class_name].regexesText,
            "new_name": null
        }
        $http.post(url, params).then(function(data) {
            console.log("Sent Post Request")
        })

        loadText();
    }

}])