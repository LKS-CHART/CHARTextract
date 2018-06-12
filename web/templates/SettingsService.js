app.service("SettingsService", [function() {
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

    return {
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
        createTrainAndValid: createTrainAndValid
    }
}])