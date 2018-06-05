app.controller("SettingsController", ["$uibModal", "LoaderService", "SettingsService", function($uibModal, $uibModalInstance, SettingsService) {
    var settingsController = this;
    settingsController.dataFile = SettingsService.dataSettings.selected;

    settingsController.openFolderDialog = function() {

        $uibModal.open({
            size: "lg",
            backdrop: true,
            windowClass: 'modal',
            controller: 'LoaderController as loaderCtrl',
            templateUrl: 'views/openFolder.html',
        })


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

    settingsController.getDataFile = function() {
        return SettingsService.dataSettings.selected
    }

    settingsController.getLabelFile = function() {
        return SettingsService.labelSettings.selected
    }

    settingsController.getRuleFolder = function() {
        return SettingsService.ruleSettings.selected
    }

}])