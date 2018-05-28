app.service('DataService', function($http, $q) {

    var deferred = $q.defer()
    var deferred2 = $q.defer()
    var deferred3 = $q.defer()

    var url = "error_report.json"
    var settingsUrl = "settings.json"
    var rulesUrl = "rules.json"

    $http.get(url).then(function (response) {
        deferred.resolve(response.data)
    })

    $http.get(settingsUrl).then(function (response) {
        deferred2.resolve(response.data)
    })

    $http.get(rulesUrl).then(function (response) {
        deferred3.resolve(response.data)
    })

    var getData = function() {
        return deferred.promise
    }

    var getSettings = function() {
        return deferred2.promise
    }

    var getRules = function() {
        return deferred3.promise
    }

    return {
        getData: getData,
        getSettings: getSettings,
        getRules: getRules,
    }

})