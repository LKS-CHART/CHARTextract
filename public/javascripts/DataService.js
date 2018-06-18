app.service('DataService', function($http, $q) {

    var deferred = $q.defer()

    var url = "/data/error_report.json"
    var url = "/" + localStorage.getItem("errorJsonPath");

    $http.get(url).then(function (response) {
        deferred.resolve(response.data)
    })

    var getData = function() {
        return deferred.promise
    }


    return {
        getData: getData,
    }

})