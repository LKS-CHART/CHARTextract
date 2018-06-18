app.controller('ErrorController', ["$sce", "DataService", function($sce,DataService) {

    var errorController = this

    var myDataPromise = DataService.getData()
    errorController.selected = null;
    errorController.selected_id = null;
    errorController.overview = true;
    errorController.match_selected = false;
    errorController.marked_data = null;
    errorController.selected_matches = null;
    errorController.pos_label = null;
    errorController.neg_label = null;

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
        errorController.data = fix_data(result)
        console.log(errorController.data)
        errorController.classes = result.classes
        var errors = errorController.data.patient_cases
        errorController.errors = {};

        if (errorController.data["Classifier Type"] === "CaptureClassifier")
        {
            var index = errorController.data["Ordered Labels"].indexOf(errorController.data["Negative Label"])
            var classes_copy = errorController.data["Ordered Labels"].slice();
            if (index !== -1) classes_copy.splice(index, 1)
            var pos_label = classes_copy[0]
            var neg_label = errorController.data["Negative Label"]

            errorController.pos_label = pos_label
            errorController.neg_label = neg_label

            errorController.errors[pos_label] = []
            errorController.errors[neg_label] = []

            angular.forEach(errors, function(error, key) {
                if (error.pred !== error.actual && error.actual === neg_label)
                {
                    errorController.errors[neg_label].push(key)
                }
                else {
                    errorController.errors[pos_label].push(key)
                }
            })
        }

        else

        {
            angular.forEach(errors, function(error, key) {
                if (error.pred != error.actual) {
                    if (errorController.classes.hasOwnProperty(error.actual)) {
                        if (angular.isUndefined(errorController.errors[error.actual]))
                        {
                            errorController.errors[error.actual] = []
                        }
                        errorController.errors[error.actual].push(key)
                    }
                }
            })
        }
    })

    errorController.gotoAnchor = function(x) {

        var newHash = String(x);
        document.getElementById(newHash).scrollIntoView(true);
        errorController.match_selected = true;
    }

    errorController.getIdInfo = function(id) {
        return errorController.data.patient_cases[id]
    }

    errorController.setSelected = function(id) {
        errorController.selected = errorController.data.patient_cases[id]
        errorController.selected_id = id
        errorController.match_selected = false;
        errorController.getSelectedMatches();
    }

    errorController.markMatch = function(id, match) {
        $("mark").unmark();

        var matched_string_r = new RegExp(match.matched_string,"im")

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


    errorController.getSentenceMatches = function(sentence_id)
    {

        $("mark").unmark();
        errorController.match_selected = true;
        var all_sentence_matches = []
        var str_id = String(sentence_id)
        for (var classname in errorController.selected.matches) {

            if (errorController.selected.matches[classname].hasOwnProperty(str_id))
            {
                var sentence_matches = errorController.selected.matches[classname][str_id]["matches"]


                for (var i = 0; i < sentence_matches.length; i++) {
                    var match_obj = sentence_matches[i];

                    var matched_string = match_obj["matches"][0]["matched_string"]

                    var primary_match = {"name": match_obj.name, "pattern": match_obj.pattern, "score": match_obj.score,
                     "effect": match_obj.effect, "aggregate_score": match_obj.aggregate_score,
                      "matched_string": matched_string, "id": str_id}

                    var matched_string_r = new RegExp(primary_match.matched_string, "im")

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

                        var matched_string_r_2 = new RegExp(secondary_match.matched_string, "im")

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

        errorController.sentence_matches = all_sentence_matches;

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
                var new_sentence = '<mark class="sMatch" style="cursor: pointer; "ng-click="errorCtrl.getSentenceMatches('+ i + ')" id="' + i + '">' + cleansed_sentence + '.</mark>'
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

    errorController.getSelectedData = function() {

        console.log("HAJSDHAKSJHd")
        errorController.marked_data = markData(errorController.selected.data, errorController.selected.matches)
        console.log(errorController.marked_data)

    }

    errorController.getSelectedMatches = function()
    {
        var sentence_ids = getSentencesWithMatches(errorController.selected.matches)
        var sentence_ids_array = Array.from(sentence_ids)
        sentence_ids_array.sort(sortNumber);
        var unrolled_primaries = []

        for (var j = 0; j < sentence_ids_array.length; j++)
        {
            var str_id= String(sentence_ids_array[j])

            for (var cname in errorController.selected.matches)
            {
                if(errorController.selected.matches[cname].hasOwnProperty(str_id))

                {
                    var sentence_matches = errorController.selected.matches[cname][str_id]["matches"]

                    for (var i = 0; i < sentence_matches.length; i++) {
                        var match_obj = sentence_matches[i];

                        var matched_string = match_obj["matches"][0]["matched_string"]

                        var primary_match = {"sentence_id": str_id, "matched_string": matched_string}

                        unrolled_primaries.push(primary_match)

                    }
                }
            }

        }

        errorController.selected_matches = unrolled_primaries
    }
}])