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


        var params = {
            "Project Settings Data": {
                "Data File": settingsController.dataFile.slice(1,settingsController.dataFile.length),
                "Label File": settingsController.labelFile.slice(1,settingsController.labelFile.length),
                "Rules Folder": settingsController.ruleFolder.slice(1,settingsController.ruleFolder.length),
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