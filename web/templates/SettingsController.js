app.controller("SettingsController", ["$uibModal", function($uibModal, $uibModalInstance) {
    var settingsController = this;

    settingsController.openFolderDialog = function() {

        $uibModal.open({
            size: "lg",
            backdrop: true,
            windowClass: 'modal',
            controller: 'LoaderController as loaderCtrl',
            templateUrl: 'views/openFolder.html'
        })

    }

    settingsController.openFileDialog = function() {

        $uibModal.open({
            size: "lg",
            backdrop: true,
            windowClass: 'modal',
            controller: 'LoaderController as loaderCtrl',
            templateUrl: 'views/openFile.html'
        })


    }



}])