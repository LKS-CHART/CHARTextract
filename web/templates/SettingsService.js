app.service("SettingsService", [function() {
    var dataSettings = {"Data File": null, "Data ID Cols": 0, "Data First Row": 1, "Data Cols": 2, "Concatenate Data": true, "selected": null}
    var labelSettings = {"Label File": null, "Label ID Cols": 0, "Label First Row": 1, "Label Cols": 2, "selected": null}
    var ruleSettings = {"Rule Folder": null, "selected": null}

    var curWorkingObj = null;

    var setCurWorkingObj = function(obj) {
        curWorkingObj = obj
    }

    var getCurWorkingObj = function() {
        return curWorkingObj;
    }

    var saveSelected = function(filepath) {
        curWorkingObj["selected"] = filepath
        console.log("BEFORE DATA SETTINGS")
        console.log(dataSettings.selected)
    }

    return {
        setCurWorkingObj: setCurWorkingObj,
        getCurWorkingObj: getCurWorkingObj,
        saveSelected: saveSelected,
        dataSettings: dataSettings,
        labelSettings: labelSettings,
        ruleSettings: ruleSettings
    }
}])