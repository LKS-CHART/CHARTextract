app.service("SettingsService", ["$q", "$http", "DataService", function($q, $http, DataService) {
    var dataSettings = {"Data File": null, "Data ID Cols": 0, "Data First Row": 1, "Data Cols": 2, "Concatenate Data": true, "selected": null}
    var labelSettings = {"Label File": null, "Label ID Cols": 0, "Label First Row": 1, "Label Cols": 2, "selected": null}
    var ruleSettings = {"Rule Folder": null, "selected": null}
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

    var url2 = "http://localhost:3000/load/variable_list"

    console.log("CALLED")
    var myDataPromise = DataService.getData();

    myDataPromise.then(function(result) {
        prevVariable = result.var_name;
    })


    console.log("SETTIGNS SERVICE INITIALIZED")


    var curWorkingObj = null;

    var setCurWorkingObj = function(obj) {
        console.log("I HAVE BEEN CALLED")
        curWorkingObj = obj
    }

    var getCurWorkingObj = function() {
        console.log("I HAVE BEEN CALLED 2")
        return curWorkingObj;
    }

    var saveSelected = function(filepath) {
        console.log("I HAVE BEEN CALLED 3")
        console.log(filepath)
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
        console.log("GET CUR VAR CALLED")
        console.log(currentVariable)
        console.log(prevVariable)
        if (currentVariable === null) {
            console.log("PREV VARIABLE")
            console.log(prevVariable)
            return prevVariable;
        }
        else {
            console.log("CURR VARIABLE")
            console.log(currentVariable)
            return currentVariable;
        }

    }

    var setCurrentVariable = function(variable) {
        currentVariable = variable;

        if (currentVariable === null) {
            console.log("YOU SET A NULL VARIABLE");
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
        dataIdCol: dataIdCol,
        dataFirstRow: dataFirstRow,
        dataCol: dataCol,
        concatenateData: concatenateData,
        labelIdCol: labelIdCol,
        labelFirstRow: labelFirstRow,
        createTrainAndValid: createTrainAndValid,
        requestVars: requestVars,
        predictionMode, predictionMode,
        getCurrentVariable: getCurrentVariable,
        setCurrentVariable: setCurrentVariable,
    }
}])