app.controller("SettingsController", ["$uibModal", function($uibModal) {
    var settingsController = this;

    settingsController.open = function() {

        $uibModal.open({
            backdrop: true,
            windowClass: 'modal',
            controller: 'LoaderController as loaderCtrl',
            templateUrl: 'openFolder.html'
        })

    }


}])