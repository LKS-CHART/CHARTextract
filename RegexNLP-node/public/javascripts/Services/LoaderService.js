app.service("LoaderService", ["$http", "$q", function($http, $q) {

    var deferred = $q.defer()
    var url = "/path/"
    var cur_path_obj = null;
    var saved_path_obj = null;

    console.log("LOADER SERVICE CREATED")


    function injectPath(path_obj) {

        var path_len = path_obj.filepath.length
        path_obj.selected=true

//        var path_constructor = {"filename": "Computer", "Root": [], "Type": "Folder", "Children": []}
        var path_constructor = angular.copy(path_obj);
        for (var i = path_len-2; i >= 0; i--) {
            var new_obj = {"filename": path_obj.filepath[i], "filepath":path_obj.filepath.slice(0,i+1), "Root": path_obj.filepath[i-1], "Type": "Folder", "Children": [], "Minimize": true}
            new_obj["Children"].push(path_constructor)
            path_constructor = new_obj;
        }

        return path_constructor;

    }

    var getInitialPath = function(path) {
        return $http.post(url,{"path": path});
    }

    var getCurPath = function() {
        return cur_path_obj
    }

    var setCurPath = function(path) {
        cur_path_obj = injectPath(path);
    }

    var saveCurPath = function(path) {
        saved_path_obj = path
    }

    var getSavePath = function() {
        return saved_path_obj;
    }

    return {
        getCurPath: getCurPath,
        setCurPath: setCurPath,
        getInitialPath: getInitialPath,
        saveCurPath: saveCurPath,
        getSavePath: getSavePath,
    }
}])