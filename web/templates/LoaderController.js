app.controller("LoaderController", ["LoaderService", "$http", "$uibModalInstance" , function(LoaderService, $http, $uibModalInstance) {
    var loaderController = this;
    var loader_data = LoaderService.getInitialPath();

    loaderController.cur_path_obj = null;

    loader_data.then(function(result) {
        loaderController.cur_path_obj = result

    })

    loaderController.requestChildren = function(path_obj) {
        var path = path_obj.root;
        var url = "http://localhost:3000/path/";

        $http.post(url, path).then(function(data) {
            console.log("SENT PATH REQUEST");
            loaderController.cur_path_obj = data.data
            LoaderService.setCurPath(loaderController.cur_path_obj)
            console.log(LoaderService.getCurPath())
        })

    }

    loaderController.cancel = function() {
        $uibModalInstance.dismiss();
    }




}])