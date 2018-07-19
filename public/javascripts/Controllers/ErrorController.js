app.controller('ErrorController', ["$sce", "DataService", "$route", function($sce,DataService, $route) {

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

    function markMatchHelper(match, id, options) {
          var match_start = match["match_start"]
          var match_end = match["match_end"]

          var new_match_start = match_start
          var new_match_end = match_end

          var actual_match_start = 0
          var actual_match_end = match_end - match_start

          var sentence = $("#" + id).text()
          sentence = " " + sentence + " "

//          console.log(sentence)
//          console.log("Match Start: " + match_start)
//          console.log("Match End: " + match_end)

          var tracker = 0;
          for (var i = 0; i < sentence.length-1; i++) {
            var t = sentence[i]
            var t1 = sentence[i+1]
            if (actual_match_start === match_start && actual_match_end === match_end)
              break;

            if ((sentence[i]==="\n" && sentence[i+1] ==="\n") || (sentence[i]==="\n" && sentence[i+1] ===" " && i !== 0)
            || (sentence[i]===" " && sentence[i+1] ==="\n" & i !== 0) || (sentence[i] === " " && sentence[i+1] === " " && i !== 0)
             || (sentence[i]==="\r" && sentence[i+1]===" ") || (sentence[i]===" " && sentence[i+1]==="\r")) {
              tracker++;

              var start_matched = false;
              if (actual_match_start < match_start) {
                new_match_start++;
                new_match_end++;
                start_matched = true;
              }

              if (!start_matched && actual_match_end < match_end) {
                new_match_end++;
              }

            } else {

              actual_match_start++;
              actual_match_end++;
            }

          }
          new_match_start  = new_match_start - 1;
          new_match_end = new_match_end - 1

          $("#" + id).markRanges([{"start": new_match_start, "length": new_match_end - new_match_start}], options)

//          console.log(tracker)

    }
    function reloadData() {
        myDataPromise.then(function(result) {
            errorController.data = fix_data(result)
            console.log(errorController.data)
            errorController.classes = result.classes
            var errors = errorController.data.patient_cases
            errorController.errors = {};
            errorController.predictionMode = result["Prediction Mode"];

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

                if (errorController.predictionMode === undefined || errorController.predictionMode === null ||
                    errorController.predictionMode === false) {

                        angular.forEach(errors, function(error, key) {
                            if (error.pred !== error.actual && error.actual === neg_label)
                            {
                                errorController.errors[neg_label].push(key)
                            }
                            else {
                                errorController.errors[pos_label].push(key)
                            }
                        })

                } else {

                    angular .forEach(errors, function(error, key) {
                        if (error.pred === errorController.data["Negative Label"]) {
                            errorController.errors[neg_label].push(key)
                        } else {

                            errorController.errors[pos_label].push(key)

                        }

                    })

                }
            }

            else

            {
                if (errorController.predictionMode === undefined || errorController.predictionMode === null ||
                    errorController.predictionMode === false) {
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
                } else

                {
                    angular.forEach(errors, function(error, key) {
                        if (angular.isUndefined(errorController.errors[error.pred]))
                        {
                            errorController.errors[error.pred] = []
                        }
                        errorController.errors[error.pred].push(key)
                    })

                }
            }
        })



    }

    reloadData();

    errorController.forceData = function() {
        myDataPromise = DataService.getDataForce();
        reloadData();

    }

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

    errorController.downloadData = function() {
        var patients = errorController.data.patient_cases

        var csv_string = '';
        if (errorController.predictionMode === undefined || errorController.predictionMode === null || errorController.predictionMode === false) {
            csv_string += '"ID","Prediction","Actual"\n';
        } else {
            csv_string += '"ID","Prediction"\n';
        }
        angular.forEach(patients, function(val, key) {
            if (errorController.predictionMode === undefined || errorController.predictionMode === null || errorController.predictionMode === false) {
                csv_string += '"' + key + '","' + val.pred + '","' + val.actual + '"\n'
            } else {
                csv_string += '"' + key + '","' + val.pred + '"\n'
            }
        })

        var encodedUri = encodeURIComponent(csv_string);
        var link = document.createElement("a");
        link.setAttribute("href", 'data:text/csv;charset=utf-8,' + encodedUri)
        link.setAttribute("download", "predictions_" + errorController.data.var_name + ".csv")

        if (document.createEvent) {
            var event = document.createEvent('MouseEvents');
            event.initEvent('click', true, true)
            link.dispatchEvent(event);
        }
        else
        {
            link.click();
        }

    }

    errorController.markMatch = function(id, match) {
        $("mark").unmark();

        if (match["effect"].startsWith("r")) {
            var options = {"className": "highlight-effect-replace", "element": "span"}
            markMatchHelper(match, id, options)
        }
        else if (match["effect"].startsWith("i")) {
            var options = {"className": "highlight-effect-ignore", "element": "span"}
            markMatchHelper(match, id, options)
        }
        else if (match["effect"].startsWith("a")) {
            var options = {"className": "highlight-effect-add", "element": "span"}
            markMatchHelper(match, id, options)
        }
        else
        {
            console.log("HERE")
            var options = {"className": "highlight", "element": "span"}
            markMatchHelper(match, id, options)
        }
    }


    errorController.getSentenceMatches = function(sentence_id)
    {

        $("mark").unmark();
        errorController.match_selected = true;
        var all_sentence_matches = []
        var str_id = String(sentence_id)

        errorController.sentence_scores = {};
        for (var classname in errorController.selected.matches) {

            if (errorController.selected.matches[classname].hasOwnProperty(str_id))
            {
                var sentence_matches = errorController.selected.matches[classname][str_id]["matches"]

                if (classname !== errorController.neg_label) {
                     var class_score = errorController.selected.matches[classname][str_id]["text_score"];
                     errorController.sentence_scores[classname] = class_score;
                }

                for (var i = 0; i < sentence_matches.length; i++) {
                    var match_obj = sentence_matches[i];

                    var matched_string = match_obj["matches"][0]["matched_string"]

                    var match_obj_py = match_obj["matches"][0]

                    var primary_match = {"name": match_obj.name, "pattern": match_obj.pattern, "score": match_obj.score,
                     "effect": match_obj.effect, "aggregate_score": match_obj.aggregate_score,
                      "matched_string": matched_string, "id": str_id, "match_start": match_obj_py.match_start, "match_end": match_obj_py.match_end}

                    var options = {"className": "highlight", "element": "span"}
                    markMatchHelper(match_obj_py, sentence_id, options)

                    all_sentence_matches.push(primary_match)

                    var secondary_matches = match_obj.secondary_regexes

                    for (var j = 0; j < secondary_matches.length; j++) {

                        var match_obj2 = secondary_matches[j];
                        var match_obj2_py = match_obj2.matches[0]
                        var secondary_match = {"name": match_obj2.name, "pattern": match_obj2.pattern, "score": match_obj2.score,
                        "effect": match_obj2.effect, "matched_string": match_obj2.matches[0].matched_string,
                        "id": str_id, "match_start": match_obj2_py.match_start, "match_end": match_obj2_py.match_end}


                        if (secondary_match["effect"].startsWith("r")) {
                            var options = {"className": "highlight-effect-replace", "element": "span"}
                            markMatchHelper(match_obj2_py, sentence_id, options)
                        }
                        else if (secondary_match["effect"].startsWith("i")) {
                            var options = {"className": "highlight-effect-ignore", "element": "span"}
                            markMatchHelper(match_obj2_py, sentence_id, options)
                        }
                        else if (secondary_match["effect"].startsWith("a")) {
                            var options = {"className": "highlight-effect-add", "element": "span"}
                            markMatchHelper(match_obj2_py, sentence_id, options)
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
//                var cleansed_sentence = sentences[i].replace(new RegExp("\n+", "i"), "<br/>");
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

        errorController.marked_data = markData(errorController.selected.data, errorController.selected.matches)

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
