app.controller("SettingsController", ["$uibModal", function($uibModal, $uibModalInstance) {
    var settingsController = this;

    settingsController.open = function() {

        $uibModal.open({
            size: "lg",
            backdrop: true,
            windowClass: 'modal',
            controller: 'LoaderController as loaderCtrl',
            templateUrl: 'views/openFolder.html'
        })

    }



}])