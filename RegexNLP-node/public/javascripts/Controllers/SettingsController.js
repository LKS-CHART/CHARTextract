app.controller("SettingsController", ["$uibModal", "LoaderService", "SettingsService", "MainRuleService", "$http", "$location", "$window", "$rootScope", "$controller", "$scope",
    function($uibModal, $uibModalInstance, SettingsService, MainRuleService, $http, $location, $window, $rootScope, $controller, $scope) {

    var settingsController = this;
    settingsController.dataFile = SettingsService.dataSettings.selected;
    settingsController.labelFile = SettingsService.labelSettings.selected;
    settingsController.validLabelFile = SettingsService.validLabelSettings.selected;
    settingsController.ruleFolder = SettingsService.ruleSettings.selected;

    settingsController.dataIdCol = SettingsService.dataIdCol
    settingsController.dataFirstRow = SettingsService.dataFirstRow
    settingsController.dataCol = SettingsService.dataCol
    settingsController.concatenateData = SettingsService.concatenateData
    settingsController.labelIdCol = SettingsService.labelIdCol
    settingsController.labelFirstRow = SettingsService.labelFirstRow
    settingsController.createTrainAndValid = SettingsService.createTrainAndValid
    settingsController.predictionMode = SettingsService.predictionMode

    var ruleCtrl_exists = false;
    var save_finished = false;

    var url = "/get_project_settings"

    $http.get(url).then(function (response) {
        var result = response.data;
        settingsController.dataCol = result["Data Cols"]
        settingsController.dataFirstRow = result["Data First Row"]
        settingsController.dataIdCol = result["Data Id Cols"]
        settingsController.concatenateData = result["Concatenate Data"]
        settingsController.labelIdCol = result["Label Id Col"]
        settingsController.labelFirstRow = result["Label First Row"]
        settingsController.createTrainAndValid = result["Create Train and Valid"]
        settingsController.predictionMode = !result.hasOwnProperty("Prediction Mode") ? false : result["Prediction Mode"]


        settingsController.dataFile = ["Computer"].concat(result["Data File"]);
        settingsController.labelFile = ["Computer"].concat(result["Label File"]);
        settingsController.ruleFolder = ["Computer"].concat(result["Rules Folder"]);
        settingsController.validLabelFile = result.hasOwnProperty("Valid Label File") ? ["Computer"].concat(result["Valid Label File"]) : ["Computer"]

        SettingsService.dataSettings.selected = settingsController.dataFile;
        SettingsService.labelSettings.selected = settingsController.labelFile;
        SettingsService.ruleSettings.selected = settingsController.ruleFolder;
        SettingsService.validLabelSettings.selected = settingsController.validLabelFile;

    })

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
            settingsController.validLabelFile = SettingsService.validLabelSettings.selected;
        });
    }

    settingsController.getDataObj = function() {
        return SettingsService.dataSettings
    }

    settingsController.getLabelObj = function() {
        return SettingsService.labelSettings
    }

    settingsController.getValidLabelObj = function() {
        return SettingsService.validLabelSettings
    }

    settingsController.getRuleObj = function() {
        return SettingsService.ruleSettings
    }

    settingsController.setWorkingObj = function(obj) {
        SettingsService.setCurWorkingObj(obj);

    }

    settingsController.getCurrentVariable = function() {
        return SettingsService.getCurrentVariable();
    }

    settingsController.setDataset = function(dataset) {
        sessionStorage.setItem('dataset', dataset);
        var p = SettingsService.getCurrentVariable() + "/" + sessionStorage.getItem("dataset") + "/" + "error_report.json";
        localStorage.setItem('errorJsonPath', p);
    }

    settingsController.run = function() {
        //Add ?mode="advanced"
        console.log("RUNNING MODE: " + MainRuleService.getMode())
        var url = "/run/" + SettingsService.getCurrentVariable() + "?mode=" + MainRuleService.getMode();

        sessionStorage.setItem("dataset", "train")

        var p = SettingsService.getCurrentVariable() + "/" + "train" + "/" + "error_report.json";
        localStorage.setItem('errorJsonPath', p);

        $rootScope.$broadcast("run_variable")
        //console.log($controller.exists('ruleCtrl') ? 'Exists' : 'Does not exist');

        window.location.href = url

    }
    $scope.$on("save_finished", function() {
        save_finished = true;
    })

    $scope.$on("saving", function() {
        save_finished = false;
    })
    $scope.$on("ruleCtrl_spawn", function() {
        ruleCtrl_exists = true;
    })

    $scope.$on("ruleCtrl_despawn", function() {
        ruleCtrl_exists = false;
    })

    settingsController.getDataset = function() {
        return sessionStorage.getItem("dataset")
    }

    settingsController.hasMultipleDatasets = function() {
        if(sessionStorage.getItem('twoSets') === null) {
            return true;
        } else {
            return sessionStorage.getItem('twoSets');
        }

    }

    settingsController.saveSettings = function() {

        SettingsService.dataIdCol = settingsController.dataIdCol
        SettingsService.dataFirstRow = settingsController.dataFirstRow
        SettingsService.dataCol = settingsController.dataCol
        SettingsService.concatenateData = settingsController.concatenateData
        SettingsService.labelIdCol = settingsController.labelIdCol
        SettingsService.labelFirstRow = settingsController.labelFirstRow
        SettingsService.createTrainAndValid = settingsController.createTrainAndValid
        SettingsService.predictionMode = settingsController.predictionMode
        var url = "/save/save_project_settings"

        console.log(settingsController.dataFile)
        console.log(settingsController.labelFile)
        console.log(settingsController.validLabelFile)
        console.log(settingsController.ruleFolder)


        if (typeof(settingsController.dataFile) === "string") {
            dataFileNorm = settingsController.dataFile.split(/[\/\\]+/)
        } else {
            dataFileNorm = settingsController.dataFile.slice(1,settingsController.dataFile.length);
        }

        if (typeof(settingsController.labelFile) === "string") {
            labelFileNorm = settingsController.labelFile.split(/[\/\\]+/)
        } else {
            labelFileNorm = settingsController.labelFile.slice(1,settingsController.labelFile.length);
        }

        if (typeof(settingsController.ruleFolder) === "string") {
            ruleFolderNorm = settingsController.ruleFolder.split(/[\/\\]+/)
        } else {
            ruleFolderNorm = settingsController.ruleFolder.slice(1,settingsController.ruleFolder.length);
        }

        if (typeof(settingsController.validLabelFile) === "string") {
            validLabelFileNorm = settingsController.validLabelFile.split(/[\/\\]+/)
        } else {
            validLabelFileNorm = settingsController.validLabelFile.slice(1,settingsController.validLabelFile.length);
        }


        var params = {
            "Project Settings Data": {
                "Data File": dataFileNorm,
                "Label File": labelFileNorm,
                "Rules Folder": ruleFolderNorm,
                "Dictionaries Folder": [],
                "Data Id Cols" : settingsController.dataIdCol,
                "Data First Row" : settingsController.dataFirstRow,
                "Data Cols" : settingsController.dataCol,
                "Concatenate Data" : settingsController.concatenateData,
                "Label Id Col" : settingsController.labelIdCol,
                "Label First Row" : settingsController.labelFirstRow,
                "Create Train and Valid" : settingsController.createTrainAndValid,
                "Prediction Mode": settingsController.predictionMode,
                "Valid Label File": validLabelFileNorm
            }
        }
        $http.post(url, params).then(function(data) {

            if ((validLabelFileNorm.length > 1 || settingsController.createTrainAndValid) && !settingsController.predictionMode) {
                sessionStorage.setItem('twoSets', "true")
                console.log("Two sets:" + sessionStorage.getItem('twoSets'))
            }
            else {
                sessionStorage.setItem('twoSets', "false")
                console.log("Two sets:" + sessionStorage.getItem('twoSets'))
            }

            sessionStorage.setItem("dataset", "train")

        })
    }

}])