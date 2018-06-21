app.controller("RuleController", ["DataService", "$http", "SettingsService", function(DataService, $http, SettingsService) {

    var ruleController = this;
    var dataPromise = DataService.getData();

    ruleController.ruleData = {};
    ruleController.previousTab = null;
    ruleController.currentTab = null;
    ruleController.currentVar = null;

    ruleController.currentVar = SettingsService.getCurrentVariable();

    ruleController.availableVars = [];

    function loadText() {
        var url = "http://localhost:3000/load/" + ruleController.currentVar;
        console.log(url)
        $http.get(url).then(function(response) {
            ruleController.ruleData = response.data
            console.log(ruleController.ruleData)

            if (Object.keys(ruleController.ruleData).length > 0) {

                var first_key = Object.keys(ruleController.ruleData)[0]
                editor.session.setValue(ruleController.ruleData[first_key]["regexesText"]);
                ruleController.currentTab = first_key;

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

    ruleController.deleteFile = function() {

    }
    ruleController.saveFile = function(class_name) {
        var first_line = editor.session.doc.$lines[0] //TODO: Replace this with new class name controller var
        var new_class_name = first_line.slice(1,first_line.length)
        ruleController.ruleData[class_name]["regexesText"] = editor.session.getValue();
        var url = "http://localhost:3000/save/" + ruleController.currentVar + "/" + new_class_name
        var params = {
            "filename": ruleController.ruleData[class_name].fileName,
            "regexes": ruleController.ruleData[class_name].regexesText
        }
        $http.post(url, params).then(function(data) {
            console.log("Sent Post Request")
        })

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
            "regexesText": "!" + temp_class_name + "\n#Change class name by editing line above"
        }

        if (ruleController.previousTab !== null) {
            ruleController.ruleData[ruleController.previousTab]["regexesText"] = editor.session.getValue();
        }

        editor.session.setValue(ruleController.ruleData[temp_class_name].regexesText)

        var url = "http://localhost:3000/save/" + ruleController.currentVar + "/" + temp_class_name;
        var params = {
            "filename": ruleController.ruleData[temp_class_name].fileName,
            "regexes": ruleController.ruleData[temp_class_name].regexesText
        }
        $http.post(url, params).then(function(data) {
            console.log("Sent Post Request")
        })
    }

}])