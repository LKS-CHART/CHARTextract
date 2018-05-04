
app.controller('ErrorController', function($scope, $sce,DataService){

    var myDataPromise = DataService.getData()
    $scope.selected = null;
    $scope.selected_id = null;
    $scope.overview = true;
    $scope.match_selected = false;
    $scope.marked_data = null;
    $scope.selected_matches = null;
    $scope.pos_label = null;
    $scope.neg_label = null;

    function fix_data(result) {

        for (var id in result.patient_cases)
        {

            if (result.patient_cases[id].data instanceof Array) {
                concat_data = result.patient_cases[id].data.join(".\n")
                result.patient_cases[id].data = concat_data
            }
        }

        return result
    }

    myDataPromise.then(function(result) {
        $scope.data = fix_data(result)
        $scope.classes = result.classes
        var errors = $scope.data.patient_cases
        $scope.errors = {};

        if ($scope.data["Classifier Type"] === "CaptureClassifier")
        {
            var index = $scope.data["Ordered Labels"].indexOf($scope.data["Negative Label"])
            var classes_copy = $scope.data["Ordered Labels"].slice();
            if (index !== -1) classes_copy.splice(index, 1)
            var pos_label = classes_copy[0]
            var neg_label = $scope.data["Negative Label"]

            $scope.pos_label = pos_label
            $scope.neg_label = neg_label

            $scope.errors[pos_label] = []
            $scope.errors[neg_label] = []

            angular.forEach(errors, function(error, key) {
                if (error.pred !== error.actual && error.actual === neg_label)
                {
                    $scope.errors[neg_label].push(key)
                }
                else {
                    $scope.errors[pos_label].push(key)
                }
            })
        }

        else

        {
            angular.forEach(errors, function(error, key) {
                if (error.pred != error.actual) {
                    if (angular.isUndefined($scope.errors[error.actual]))
                    {
                        $scope.errors[error.actual] = []
                    }
                    $scope.errors[error.actual].push(key)
                }
            })
        }
    })

    $scope.gotoAnchor = function(x) {

        var newHash = String(x);
        document.getElementById(newHash).scrollIntoView(true);
        $scope.match_selected = true;
    }

    $scope.getIdInfo = function(id) {
        return $scope.data.patient_cases[id]
    }

    $scope.setSelected = function(id) {
        $scope.selected = $scope.data.patient_cases[id]
        $scope.selected_id = id
        $scope.match_selected = false;
        $scope.getSelectedMatches();
    }

    $scope.markMatch = function(id, match) {
        $("mark").unmark();

        var matched_string_r = new RegExp(match.pattern,"im")

        if (match["effect"].startsWith("r")) {
            $("#" + id).markRegExp(matched_string_r, {
            "className": "highlight-effect-replace",
            "element": "span", "acrossElements": true})
        }
        else if (match["effect"].startsWith("i")) {
            $("#" + id).markRegExp(matched_string_r, {
            "className": "highlight-effect-ignore",
            "element": "span", "acrossElements": true})
        }
        else if (match["effect"].startsWith("a")) {
            $("#" + id).markRegExp(matched_string_r, {
            "className": "highlight-effect-add",
            "element": "span", "acrossElements": true})
        }
        else
        {
            $("#" + id).markRegExp(matched_string_r, {"className": "highlight",
            "element": "span", "acrossElements": true})
        }
    }


    $scope.getSentenceMatches = function(sentence_id)
    {

        $("mark").unmark();
        $scope.match_selected = true;
        var all_sentence_matches = []
        var str_id = String(sentence_id)
        for (var classname in $scope.selected.matches) {

            if ($scope.selected.matches[classname].hasOwnProperty(str_id))
            {
                var sentence_matches = $scope.selected.matches[classname][str_id]["matches"]


                for (var i = 0; i < sentence_matches.length; i++) {
                    var match_obj = sentence_matches[i];

                    var matched_string = match_obj["matches"][0]["matched_string"]

                    var primary_match = {"name": match_obj.name, "pattern": match_obj.pattern, "score": match_obj.score,
                     "effect": match_obj.effect, "aggregate_score": match_obj.aggregate_score,
                      "matched_string": matched_string, "id": str_id}

                    var matched_string_r = new RegExp(match_obj.pattern, "i")
                    $("#" + str_id).markRegExp(matched_string_r, {"className": "highlight",
                    "acrossElements": true,
                    "element": "span"})

                    all_sentence_matches.push(primary_match)

                    var secondary_matches = match_obj.secondary_regexes

                    for (var j = 0; j < secondary_matches.length; j++) {

                        var match_obj2 = secondary_matches[j];
                        var secondary_match = {"name": match_obj2.name, "pattern": match_obj2.pattern, "score": match_obj2.score,
                        "effect": match_obj2.effect, "matched_string": match_obj2.matches[0].matched_string,
                        "id": str_id}

                        var matched_string_r_2 = new RegExp(match_obj2.pattern, "im")

                        if (secondary_match["effect"].startsWith("r")) {
                            $("#" + str_id).markRegExp(matched_string_r_2, {
                            "className": "highlight-effect-replace",
                            "element": "span", "acrossElements": true})
                        }
                        else if (secondary_match["effect"].startsWith("i")) {
                            $("#" + str_id).markRegExp(matched_string_r_2, {
                            "className": "highlight-effect-ignore",
                            "element": "span", "acrossElements": true})
                        }
                        else if (secondary_match["effect"].startsWith("a")) {
                            $("#" + str_id).markRegExp(matched_string_r_2, {
                            "className": "highlight-effect-add",
                            "element": "span", "acrossElements": true})
                        }
                        all_sentence_matches.push(secondary_match)

                    }

                }

            }


        }

        $scope.sentence_matches = all_sentence_matches;

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

                  var cleansed_sentence = sentences[i]
//                var cleansed_sentence = sentences[i].replace(new RegExp("\n+", "i"), " ");
//                console.log(sentences[i])
//                console.log(cleansed_sentence)
//                console.log("CLEANY CLEANY")
                var new_sentence = '<mark class="sMatch" style="cursor: pointer; "ng-click="getSentenceMatches('+ i + ')" id="' + i + '">' + cleansed_sentence + '.</mark>'
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

    function sortNumber(a,b) {
        return a-b;
    }

//    $scope.reload = function() {
//        var container = document.getElementById("text");
//        var content = container.innerHTML;
//        container.innerHTML = content;
//        console.log("CHANGEd")
//    }

    $scope.getSelectedData = function() {

        console.log("HAJSDHAKSJHd")
        $scope.marked_data = markData($scope.selected.data, $scope.selected.matches)

//        return $sce.trustAsHtml(marked_data)
    }

    $scope.getSelectedMatches = function()
    {
        var sentence_ids = getSentencesWithMatches($scope.selected.matches)
        var sentence_ids_array = Array.from(sentence_ids)
        sentence_ids_array.sort(sortNumber);
        var unrolled_primaries = []

        for (var j = 0; j < sentence_ids_array.length; j++)
        {
            var str_id= String(sentence_ids_array[j])

            for (var cname in $scope.selected.matches)
            {
                if($scope.selected.matches[cname].hasOwnProperty(str_id))

                {
                    var sentence_matches = $scope.selected.matches[cname][str_id]["matches"]

                    for (var i = 0; i < sentence_matches.length; i++) {
                        var match_obj = sentence_matches[i];

                        var matched_string = match_obj["matches"][0]["matched_string"]

                        var primary_match = {"sentence_id": str_id, "matched_string": matched_string}

                        unrolled_primaries.push(primary_match)

                    }
                }
            }

        }

        $scope.selected_matches = unrolled_primaries
    }
})