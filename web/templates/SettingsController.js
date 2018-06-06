app.controller("SettingsController", ["$uibModal", "LoaderService", "SettingsService", function($uibModal, $uibModalInstance, SettingsService) {
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

}])