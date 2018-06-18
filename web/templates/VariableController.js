app.controller("VariableController", ["SettingsService", "$http", function(SettingsService, $http) {
    var variableController = this;

    variableController.currentVariable = null;
    variableController.availableVariables = [];

    variableController.curVarLabelCol = 1;
    variableController.curVarDictionaries = "";
    variableController.python = false;
    variableController.usePreprocessor = true;

    var url = "http://localhost:3000/load/variable_settings/"

    if (variableController.currentVariable === null) {
        variableController.currentVariable = SettingsService.getCurrentVariable();
    }

    SettingsService.requestVars().then(function(result) {
        console.log("DONE GETTING VAR LIST")
        variableController.availableVariables = result["Variable List"]

    })

    variableController.saveSettings = function() {
        SettingsService.setCurrentVariable(variableController.currentVariable);
    }

    variableController.getCurVarSettings = function() {


    }

}])
