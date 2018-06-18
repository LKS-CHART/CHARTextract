app.controller("VariableController", ["SettingsService", "$http", function(SettingsService, $http) {
    var variableController = this;

    variableController.currentVariable = null;
    variableController.availableVariables = [];

    variableController.curVarLabelCol = 1;
    variableController.curVarDictionaries = "";
    variableController.python = false;
    variableController.usePreprocessor = false;

    var url = "http://localhost:3000/load/variable_settings"

    if (variableController.currentVariable === null) {
        variableController.currentVariable = SettingsService.getCurrentVariable();
    }

    function getVariableSettings() {
        var url = "http://localhost:3000/load/variable_settings/" + variableController.currentVariable;

        $http.get(url).then(function(result) {
            var data = result.data;

            variableController.curVarLabelCol = data["Label Col"];

            if (data.hasOwnProperty("Pwds")) {
                variableController.curVarDictionaries = data["Pwds"].join(",");
            }
            else {
                variableController.curVarDictionaries = "";
            }

            if (data.hasOwnProperty("Specify Function with Python")) {
                variableController.python = data["Specify Function with Python"];
            }
            else {
                variableController.python = false;
            }

            if (data.hasOwnProperty("Use Preprocessor")) {
                variableController.usePreprocessor = data["Use Preprocessor"];
            }
            else {
                variableController.usePreprocessor = false;
            }

        })

    }

    getVariableSettings();

    SettingsService.requestVars().then(function(result) {
        console.log("DONE GETTING VAR LIST")
        variableController.availableVariables = result["Variable List"]

    })

    variableController.saveSettings = function() {
        SettingsService.setCurrentVariable(variableController.currentVariable);


    }

    variableController.getCurVarSettings = function() {
        console.log("IN VARIABLE CONTROLLER GET CUR VAR SETTINGS")

        getVariableSettings();
    }

}])