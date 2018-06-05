app.controller("LoaderController", ["LoaderService", "$http", "$uibModalInstance" , function(LoaderService, $http, $uibModalInstance) {
    var loaderController = this;
    var loader_data = LoaderService.getInitialPath();


    loader_data.then(function(result) {
        LoaderService.setCurPath(result)
    })
    loaderController.getCurPath = function() {
        return LoaderService.getCurPath();
    }

    loaderController.save = function() {

    }

    loaderController.cancel = function() {
        $uibModalInstance.dismiss();
    }

}])
