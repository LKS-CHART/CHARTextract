app.controller("VariableController", ["SettingsService", "$http", function(SettingsService, $http) {
    var variableController = this;

    variableController.currentVariable = SettingsService.currentVariable;
    variableController.availableVariables = [];

    variableController.curVarLabelCol = 1;
    variableController.curVarDictionaries = "";
    variableController.python = false;
    variableController.usePreprocessor = true;


    SettingsService.requestVars().then(function(result) {
        console.log("DONE GETTING VAR LIST")
        variableController.availableVariables = result["Variable List"]
    })

    variableController.saveSettings = function() {
        SettingsService.currentVariable = variableController.currentVariable;
    }

}])
