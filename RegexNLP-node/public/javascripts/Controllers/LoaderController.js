app.controller("LoaderController", ["LoaderService", "SettingsService", "$http", "$uibModalInstance" , function(LoaderService, SettingsService, $http, $uibModalInstance) {
    var loaderController = this;
    console.log("Get Working Object");
    console.log(SettingsService.getCurWorkingObj().selected.last);
    var loader_data = LoaderService.getInitialPath(SettingsService.getCurWorkingObj().selected);

    loader_data.then(function(response){
        console.log(response.data);
        LoaderService.setCurPath(response.data);
    });

    loaderController.getCurPath = function() {
        return LoaderService.getCurPath();
    };

    loaderController.save = function() {
        $uibModalInstance.close();
    };

    loaderController.cancel = function() {
        $uibModalInstance.dismiss();
    }

}]);