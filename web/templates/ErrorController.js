app.controller('ErrorController', function($scope, $sce, DataService){

    var myDataPromise = DataService.getData()
    $scope.selected = null;
    $scope.selected_id = null;
    $scope.overview = true;
    $scope.match_selected = false;

    myDataPromise.then(function(result) {
        $scope.data = result
        $scope.classes = result.classes
        var errors = $scope.data.patient_cases
        $scope.errors = {};

        angular.forEach(errors, function(error, key) {
            if (error.pred != error.actual) {
                if (angular.isUndefined($scope.errors[error.actual]))
                {
                    $scope.errors[error.actual] = []
                }
                $scope.errors[error.actual].push(key)
            }
        })
    })

    $scope.getIdInfo = function(id) {
        return $scope.data.patient_cases[id]
    }

    $scope.setSelected = function(id) {
        $scope.selected = $scope.data.patient_cases[id]
        $scope.selected_id = id
    }

    $scope.getSentenceMatches = function(sentence_id)
    {

        var all_sentence_matches = []
        var str_id = String(sentence_id)
        for (var classname in $scope.selected.matches) {

            if ($scope.selected.matches[classname].hasOwnProperty(str_id))
            {
                sentence_matches = $scope.selected.matches[classname][str_id]


                for (var i = 0; i < sentence_matches.length; i++) {
                    var match_obj = sentence_matches[i];

                    matched_string = match_obj["matches"][0]["matched_string"]

                    var primary_match = {"name": match_obj.name, "pattern": match_obj.pattern, "score": match_obj.score, "effect": match_obj.pattern, "aggregate_score": match_obj.aggregate_score, "matched_string": matched_string}

                    all_sentence_matches.push(primary_match)

                    var secondary_matches = match_obj.secondary_regexes

                    for (var j = 0; j < secondary_matches.length; j++) {

                        var match_obj2 = secondary_matches[j];
                        var secondary_match = {"name": match_obj2.name, "pattern": match_obj2.pattern, "score": match_obj2.score,
                        "effect": match_obj2.pattern, "matched_string": match_obj2.matches[0].matched_string}

                        all_sentence_matches.push(secondary_match)

                    }

                }

            }


        }

    }

    function getSentencesWithMatches(matches) {

        var sentence_set = new Set();

        for (var classname in matches) {

            for (var key in matches[classname]) {

                sentence_set.add(parseInt(key))
            }
        }

        return sentence_set

    }


    function markData(data, matches)
    {

        var new_data = "";
        var sentences = data.split(".");
        var sentences_with_matches = getSentencesWithMatches(matches)

        for (var i = 0; i < sentences.length; i++)
        {

            if (sentences_with_matches.has(i)) {

                var new_sentence = '<mark id="' + i + '">' + sentences[i] + '.</mark>'
                new_data += new_sentence
            }
            else
            {
                new_data += sentences[i]

                if (sentences[i] != '') {
                    new_data += '.'
                }
            }

        }

        return new_data

    }

    $scope.getSelectedData = function() {

        marked_data = markData($scope.selected.data, $scope.selected.matches)
        return $sce.trustAsHtml(marked_data)
    }

})
