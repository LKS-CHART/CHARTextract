app.service('DataService', function($http, $q) {

    var deferred = $q.defer()

    var url = "";
    
    if (localStorage.getItem("errorJsonPath") === null) {
        url = "/data/error_report.json";
    } else {
        url = "/" + localStorage.getItem("errorJsonPath");
    }

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
