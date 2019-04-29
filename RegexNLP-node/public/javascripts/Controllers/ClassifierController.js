app.controller("ClassifierController", ["SettingsService", "$http", function(SettingsService, $http) {
    var classifierController = this;

    classifierController.availableClassifiers = {"RegexClassifier": "biases", "CaptureClassifier":"capture_biases"}

    classifierController.currentClassifier = "RegexClassifier"
    classifierController.negativeLabel = "None"

    classifierController.biases = [];

    function getClassifierSettings() {

        var url = "/load/classifier_settings/" + SettingsService.getCurrentVariable();

        $http.get(url).then(function(result) {
            var data = result.data;
            classifierController.currentClassifier = data["Classifier Type"];
            classifierController.negativeLabel = "None";
            classifierController.biases = [];

            if (data.hasOwnProperty("Classifier Args")) {
                var classifierArgs = data["Classifier Args"];

                if (classifierArgs.hasOwnProperty("negative_label")) {
                    classifierController.negativeLabel = classifierArgs["negative_label"]
                }

                if (classifierArgs.hasOwnProperty("biases") || classifierArgs.hasOwnProperty("capture_biases")) {
                    var biases = classifierArgs.biases || classifierArgs.capture_biases
                    console.log(biases)

                    for (var key in biases) {
                        classifierController.biases.push(angular.copy({"class": key, "bias": biases[key]}))
                    }
                }
            }

        })
    }

    getClassifierSettings();

    classifierController.getCurrentVariable = function() {
        return SettingsService.getCurrentVariable()
    }

    classifierController.addBias = function() {
         classifierController.biases.push(angular.copy({"class": "", "bias": 0}))
    }

    classifierController.removeBias = function(index) {
        classifierController.biases.splice(index,1);
    }

    classifierController.saveSettings = function() {

        var url = "/save/save_classifier_settings/" + SettingsService.getCurrentVariable();

        var params = {"Classifier Type": classifierController.currentClassifier, "Classifier Args": {}}
        var neg_label = "None"
        if (classifierController.negativeLabel !== "") {
            neg_label = classifierController.negativeLabel
        }

        params["Classifier Args"].negative_label = neg_label

        if (classifierController.biases.length > 0) {
            var biases_dict = {};

               classifierController.biases.forEach(val => {
                    console.log(val)
                   biases_dict[val.class] = val.bias
               })

            params["Classifier Args"][classifierController.availableClassifiers[classifierController.currentClassifier]] = biases_dict
        }

        $http.post(url, {"Classifier Settings": params}).then(function() {
            console.log("Saved Classifier Settings");
            SettingsService.setCurrentNegativeLabel(neg_label)

        })

    }


}])