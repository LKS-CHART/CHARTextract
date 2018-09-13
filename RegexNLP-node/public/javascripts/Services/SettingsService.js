app.service("SettingsService", ["$q", "$http", "DataService", function($q, $http, DataService) {
    var dataSettings = {"selected": null}
    var labelSettings = {"selected": null}
    var ruleSettings = {"selected": null}
    var validLabelSettings = {"selected": null}
    var dataIdCol = 0
    var dataFirstRow = 1
    var dataCol = 2
    var concatenateData = true;
    var labelIdCol = 0
    var labelFirstRow = 1
    var createTrainAndValid = true;
    var predictionMode = false;

    var currentVariable = null;
    var prevVariable = null;

    var deferred = $q.defer()

    var url2 = "/load/variable_list"

    var negativeLabel = "None";

    var myDataPromise = DataService.getData();

    $http.get("/run/get_response_status").then(function(response) {
        var status = response.data[0];

        if (status["status"] === 404) {
            alert(status["message"])
        }

    })

    myDataPromise.then(function(result) {
        prevVariable = result.var_name;
    })

    console.log("SETTIGNS SERVICE LOADED")

    var curWorkingObj = null;

    var setCurWorkingObj = function(obj) {
        curWorkingObj = obj
    }

    var getCurWorkingObj = function() {
        return curWorkingObj;
    }

    var saveSelected = function(filepath) {
        curWorkingObj["selected"] = filepath
    }

    var getSettingsData = function() {

        return deferred.promise
    }

    var requestVars = function() {
        var deferred2 = $q.defer()
        $http.get(url2).then(function (response) {
            deferred2.resolve(response.data)
        })
        return deferred2.promise;
    }

    var getCurrentVariable = function() {
        if (currentVariable === null) {

            if(localStorage.getItem("currentVariable") === null) {

                return prevVariable
            }

            return localStorage.getItem("currentVariable");
        }
        else {
            return currentVariable;
        }

    }

    var getCurrentNegativeLabel = function() {
        if (sessionStorage.getItem("currentNegativeLabel") === null || sessionStorage.getItem("currentNegativeLabel") === undefined) {
            return "None"
        }
        return sessionStorage.getItem("currentNegativeLabel");
    }

    var setCurrentNegativeLabel = function(negative_label) {
        sessionStorage.setItem("currentNegativeLabel", negative_label)
    }

    var setCurrentVariable = function(variable) {
        currentVariable = variable;

        if (currentVariable === null) {
        }
    }

    return {
        getSettings: getSettingsData,
        setCurWorkingObj: setCurWorkingObj,
        getCurWorkingObj: getCurWorkingObj,
        saveSelected: saveSelected,
        dataSettings: dataSettings,
        labelSettings: labelSettings,
        ruleSettings: ruleSettings,
        validLabelSettings: validLabelSettings,
        dataIdCol: dataIdCol,
        dataFirstRow: dataFirstRow,
        dataCol: dataCol,
        concatenateData: concatenateData,
        labelIdCol: labelIdCol,
        labelFirstRow: labelFirstRow,
        createTrainAndValid: createTrainAndValid,
        requestVars: requestVars,
        predictionMode: predictionMode,
        getCurrentVariable: getCurrentVariable,
        setCurrentVariable: setCurrentVariable,
        getCurrentNegativeLabel: getCurrentNegativeLabel,
        setCurrentNegativeLabel: setCurrentNegativeLabel
    }
}])