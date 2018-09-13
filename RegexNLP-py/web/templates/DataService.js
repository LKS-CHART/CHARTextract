app.service('DataService', function($http, $q) {

    var deferred = $q.defer()


    if(localStorage.getItem("errorJsonPath") === null || localStorage.getItem("errorJsonPath") === undefined) {
        var url = "/data/error_report.json"
    }
    else
    {

        var url = "/" + localStorage.getItem("errorJsonPath");
    }


    //var url = "/data/error_report.json"
    $http.get(url).then(function (response) {
        deferred.resolve(response.data)
    })

    var getData = function() {
        return deferred.promise
    }

    var getDataForce = function() {

        var url = "/" + localStorage.getItem("errorJsonPath");
        var deferred = $q.defer()

        console.log(url)

        $http.get(url).then(function (response) {
            deferred.resolve(response.data)
        })

        return deferred.promise

    }


    return {
        getData: getData,
        getDataForce: getDataForce
    }

})