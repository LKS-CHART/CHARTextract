app.controller("SettingsController", ["$uibModal", "LoaderService", "SettingsService", "$http", function($uibModal, $uibModalInstance, SettingsService, $http) {
    var settingsController = this;
    settingsController.dataFile = SettingsService.dataSettings.selected;
    settingsController.labelFile = SettingsService.labelSettings.selected;
    settingsController.ruleFolder = SettingsService.ruleSettings.selected;
    settingsController.dataIdCol = SettingsService.dataIdCol
    settingsController.dataFirstRow = SettingsService.dataFirstRow
    settingsController.dataCol = SettingsService.dataCol
    settingsController.concatenateData = SettingsService.concatenateData
    settingsController.labelIdCol = SettingsService.labelIdCol
    settingsController.labelFirstRow = SettingsService.labelFirstRow
    settingsController.createTrainAndValid = SettingsService.createTrainAndValid

    var settingsPromise = SettingsService.getSettings();

    settingsPromise.then(function(result) {

        settingsController.dataCol = result["Data Cols"]
        settingsController.dataFirstRow = result["Data First Row"]
        settingsController.dataIdCol = result["Data Id Cols"]
        settingsController.concatenateData = result["Concatenate Data"]
        settingsController.labelIdCol = result["Label Id Col"]
        settingsController.labelFirstRow = result["Label First Row"]
        settingsController.createTrainAndValid = result["Create Train and Valid"]

        settingsController.dataFile = ["Computer"].concat(result["Data File"]);
        settingsController.labelFile = ["Computer"].concat(result["Label File"]);
        settingsController.ruleFolder = ["Computer"].concat(result["Rules Folder"]);

        SettingsService.dataSettings.selected = settingsController.dataFile;
        SettingsService.labelSettings.selected = settingsController.labelFile;
        SettingsService.ruleSettings.selected = settingsController.ruleFolder;

    });

    settingsController.openFolderDialog = function() {

        $uibModal.open({
            size: "lg",
            backdrop: true,
            windowClass: 'modal',
            controller: 'LoaderController as loaderCtrl',
            templateUrl: 'views/openFolder.html',
        }).result.then(function() {
            settingsController.ruleFolder = SettingsService.ruleSettings.selected;
        });


    }
    settingsController.openFileDialog = function() {

        $uibModal.open({
            size: "lg",
            backdrop: true,
            windowClass: 'modal',
            controller: 'LoaderController as loaderCtrl',
            templateUrl: 'views/openFile.html',
        }).result.then(function() {
            settingsController.dataFile = SettingsService.dataSettings.selected;
            settingsController.labelFile = SettingsService.labelSettings.selected;
        });



    }

    settingsController.getDataObj = function() {
        return SettingsService.dataSettings
    }

    settingsController.getLabelObj = function() {
        return SettingsService.labelSettings
    }

    settingsController.getRuleObj = function() {
        return SettingsService.ruleSettings
    }

    settingsController.setWorkingObj = function(obj) {
        SettingsService.setCurWorkingObj(obj);

    }

    settingsController.getCurrentVariable = function() {
        console.log("IN SETTINGS CONTROLLER CALLING GET CURRENT VARIABLE");
        return SettingsService.getCurrentVariable();
    }

    settingsController.run = function() {
        console.log("BEFORE CURRENT VARIABLE");
        var url = "http://localhost:3000/run/" + SettingsService.getCurrentVariable();
        $http.get(url).then(function(result) {
            console.log("PLEASE DON'T BREAK");
        })
    }

    settingsController.saveSettings = function() {

        SettingsService.dataIdCol = settingsController.dataIdCol
        SettingsService.dataFirstRow = settingsController.dataFirstRow
        SettingsService.dataCol = settingsController.dataCol
        SettingsService.concatenateData = settingsController.concatenateData
        SettingsService.labelIdCol = settingsController.labelIdCol
        SettingsService.labelFirstRow = settingsController.labelFirstRow
        SettingsService.createTrainAndValid = settingsController.createTrainAndValid
        var url = "http://localhost:3000/save/save_project_settings"

        console.log(settingsController.dataFile)
        console.log(settingsController.labelFile)
        console.log(settingsController.ruleFolder)

        dataFileNorm = settingsController.dataFile.slice(1,settingsController.dataFile.length);
        labelFileNorm = settingsController.labelFile.slice(1,settingsController.labelFile.length);
        ruleFolderNorm = settingsController.ruleFolder.slice(1,settingsController.ruleFolder.length);

        var params = {
            "Project Settings Data": {
                "Data File": dataFileNorm,
                "Label File": labelFileNorm,
                "Rules Folder": ruleFolderNorm,
                "Dictionaries Folder": "dictionaries",
                "Data Id Cols" : settingsController.dataIdCol,
                "Data First Row" : settingsController.dataFirstRow,
                "Data Cols" : settingsController.dataCol,
                "Concatenate Data" : settingsController.concatenateData,
                "Label Id Col" : settingsController.labelIdCol,
                "Label First Row" : settingsController.labelFirstRow,
                "Create Train and Valid" : settingsController.createTrainAndValid,
            }
        }
        $http.post(url, params).then(function(data) {
            console.log(data)
            console.log("Sent Save Settings Request")
            console.log(settingsController.dataFile)
            console.log(settingsController.labelFile)
            console.log(settingsController.ruleFolder)
            console.log(SettingsService.createTrainAndValid)
        }).then(function() {
            console.log(settingsController.dataFile)
            console.log(settingsController.labelFile)
            console.log(settingsController.ruleFolder)
        });
    }

}])