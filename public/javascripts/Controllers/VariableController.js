app.controller("VariableController", ["SettingsService", "$http", function(SettingsService, $http) {
    var variableController = this;

    variableController.currentVariable = null;
    variableController.availableVariables = [];

    variableController.curVarLabelCol = 1;
    variableController.curVarDictionaries = "";
    variableController.python = false;
    variableController.usePreprocessor = false;

    variableController.editMode = false;

    var url = "/load/variable_settings"

    if (variableController.currentVariable === null) {
        variableController.currentVariable = SettingsService.getCurrentVariable();
    }


    function getVariableSettings() {
        if (variableController.currentVariable === null) {
            url = "/data/default_variable_settings";
        } else {
            url = "/load/variable_settings/" + variableController.currentVariable;
        }
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
        variableController.availableVariables = result["Variable List"]

    })

    variableController.saveSettings = function() {
        var url2 = "/save/save_variable_settings/" + variableController.currentVariable;

        SettingsService.setCurrentVariable(variableController.currentVariable);

        var arrayfied_dictionaries = variableController.curVarDictionaries === "" ? [] :
                                            variableController.curVarDictionaries.split(",")

        var arrayfied_label_cols = null;

        if (typeof(variableController.curVarLabelCol) === "number" || typeof(variableController.curVarLabelCol) === "object") {
            arrayfied_label_cols = variableController.curVarLabelCol
        }

        else {
            arrayfied_label_cols = variableController.curVarLabelCol.split(",");

            for (var i = 0; i < arrayfied_label_cols.length; i++) {
                arrayfied_label_cols[i] = parseInt(arrayfied_label_cols[i])
            }
        }

        var params = {
            "Variable Settings": {
                "Label Col": arrayfied_label_cols,
                "Pwds": arrayfied_dictionaries,
                "Specify Function with Python": variableController.python,
                "Use Preprocessor": variableController.usePreprocessor
            }
        }

        $http.post(url2, params).then(function(data) {
            console.log("Sent Save Variable Settings Request")

            var url3 = "/load/classifier_settings/" + SettingsService.getCurrentVariable();

            $http.get(url3).then(function(result) {
                var data = result.data;

                    if (data.hasOwnProperty("Classifier Args") && data["Classifier Args"].hasOwnProperty("negative_label")) {
                        SettingsService.setCurrentNegativeLabel(data["Classifier Args"]["negative_label"])
                    } else {

                        SettingsService.setCurrentNegativeLabel("None")
                    }
                })
            })

        variableController.editMode = false;

        localStorage.setItem("currentVariable", variableController.currentVariable);

        SettingsService.requestVars().then(function(result) {
            variableController.availableVariables = result["Variable List"]
        })
    }

    variableController.getCurVarSettings = function() {
        getVariableSettings();
    }

    variableController.savedVariable = function() {
        return SettingsService.getCurrentVariable();
    }


    variableController.addVariable = function() {
        variableController.currentVariable = "";
        variableController.editMode = true;
        variableController.curVarLabelCol = 1;
        variableController.curVarDictionaries = "";
        variableController.python = false;
        variableController.usePreprocessor = false;
    }

}])