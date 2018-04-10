app.service('DataService', function($http, $q) {

    var deferred = $q.defer()
    var url = "error_report.json"
    $http.get(url).then(function (response) {
        deferred.resolve(response.data)
    })

    this.getData = function () {
        return deferred.promise;
    }


})