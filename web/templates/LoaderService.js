app.service("LoaderService", ["$http", "$q", function($http, $q) {

    var deferred = $q.defer()
    var url = "http://localhost:3000/path/"
    var cur_path_obj = null;


    function injectPath(path_obj) {

        var path_len = path_obj.filepath.length
        path_obj.selected=true

        console.log(path_obj.filepath)
        console.log("INJECT BEING CALLED")

//        var path_constructor = {"filename": "Computer", "Root": [], "Type": "Folder", "Children": []}
        var path_constructor = angular.copy(path_obj);
        for (var i = path_len-2; i >= 0; i--) {
            var new_obj = {"filename": path_obj.filepath[i], "filepath":path_obj.filepath.slice(0,i+1), "Root": path_obj.filepath[i-1], "Type": "Folder", "Children": [], "Minimize": true}
            new_obj["Children"].push(path_constructor)
            path_constructor = new_obj;
        }

        console.log(path_constructor)
        return path_constructor;

    }

    $http.get(url).then(function (response) {
        cur_path_obj = response.data
        deferred.resolve(response.data)
    })
    var getInitialPath = function() {
        return deferred.promise
    }

    var getCurPath = function() {
        return cur_path_obj
    }

    var setCurPath = function(path) {
        cur_path_obj = injectPath(path);
    }

    return {
        getCurPath: getCurPath,
        setCurPath: setCurPath,
        getInitialPath: getInitialPath,
    }
}])
