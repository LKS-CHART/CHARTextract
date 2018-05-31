app.service("LoaderService", ["$http", "$q", function($http, $q) {

    var deferred = $q.defer()
    var url = "http://localhost:3000/path/"
    var cur_path_obj = null;

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
        cur_path_obj = path;
    }

    return {
        getCurPath: getCurPath,
        setCurPath: setCurPath,
        getInitialPath: getInitialPath,
    }
}])
