app.controller("LoaderController", ["LoaderService", "$http", "$uibModalInstance" , function(LoaderService, $http, $uibModalInstance) {
    var loaderController = this;
    var loader_data = LoaderService.getInitialPath();


    loader_data.then(function(result) {
        console.log("Loader data?")
        console.log(result)

        if (LoaderService.getCurPath() === null) {
            LoaderService.setCurPath(result)
        }
    })
    loaderController.getCurPath = function() {
        return LoaderService.getCurPath();
    }

    loaderController.save = function() {
        $uibModalInstance.close();
    }

    loaderController.cancel = function() {
        $uibModalInstance.dismiss();
    }

}])
