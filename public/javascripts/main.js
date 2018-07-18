app = angular.module('app', ['ngRoute', 'RecursionHelper', 'ui.bootstrap']).config(['$routeProvider', function($routeProvider) {
    $routeProvider.
    when('/view', {
        templateUrl: 'views/view.html',
    }).
    when('/overview', {
        templateUrl: 'views/overview.html',
    }).
    when('/settings', {
        templateUrl: 'views/settings.html',
        controller: "SettingsController",
        controllerAs: "settingsCtrl"
    }).
    when('/regexes', {
        templateUrl: 'views/regexes.html',
        controller: "RuleController",
        controllerAs: "ruleCtrl"
    }).
    when('/variable_settings', {
        templateUrl: 'views/variableSettings.html',
        controller: "VariableController",
        controllerAs: "variableCtrl"
    }).
    when('/rule_simp', {
        templateUrl: 'views/rulesimp.html',
        controller: "RuleControllerSimp",
        controllerAs: "ruleCtrl"
    }).
    when('/classifier_settings', {
        templateUrl: 'views/classifierSettings.html',
        controller: "ClassifierController",
        controllerAs: "classifierCtrl"
    })
}])
//
//app.config(['$provide', function($provide) {
//    $provide.decorator("$controller", ["$delegate", function($delegate) {
//        $delegate.exists = function(controllerName) {
//            if(typeof window[controllerName] == 'function') {
//                return true;
//            }
//            try {
//                $controller(controllerName);
//                return true;
//            } catch (error) {
//                return !(error instanceof TypeError);
//            }
//        }
//
//        return $delegate
//    }])
//}])
app.directive('ngHtmlCompile', function($compile) {
    return {
	    restrict: 'A',
	    link: function(scope, element, attrs) {
		scope.$watch(attrs.ngHtmlCompile, function(newValue, oldValue) {
		    element.html(newValue);
		    $compile(element.contents())(scope);
		});
	    }
	}
})

app.directive("tree", function(RecursionHelper, LoaderService, $http, SettingsService) {
    return {
        restrict: "E",
        scope: {
            node: "=node",
            display_folder: "=displayOnlyFolder",
        },
        templateUrl: "views/fileView.html",
        compile: function(element) {
            return RecursionHelper.compile(element, function(scope, iElement, iAttrs, controller, transcludeFn) {
                scope.navigateToItem = function(node) {
                    var url = "http://localhost:3000/path/"
                    var params = {"path": node.filepath}
                    $http.post(url, params).then(function(data) {
                        console.log("SENT PATH REQUEST");
                        LoaderService.setCurPath(data.data);
                        if(node.Type === "File") {
                            SettingsService.saveSelected(data.data.filepath)
                        }
//                        console.log(LoaderService.getSavePath(data.data.filepath))
//                        console.log(LoaderService.getCurPath())
//                        $rootScope.$broadcast('tree', 'treeSave')
                    })
                }

            })
        }

    }
})

app.directive("treeF", function(RecursionHelper, LoaderService, $http, SettingsService) {
    return {
        restrict: "E",
        scope: {
            node: "=node",
            display_folder: "=displayOnlyFolder"
        },
        templateUrl: "views/folderView.html",
        compile: function(element) {
            return RecursionHelper.compile(element, function(scope, iElement, iAttrs, controller, transcludeFn) {
                scope.navigateToItem = function(node) {
                    var url = "http://localhost:3000/path/"
                    var params = {"path": node.filepath}
                    $http.post(url, params).then(function(data) {
                        console.log("SENT PATH REQUEST");
                        LoaderService.setCurPath(data.data);

                        if(node.Type === "Folder") {
                            SettingsService.saveSelected(data.data.filepath)
                        }
                        console.log(LoaderService.getCurPath())
                    })
                }

            })
        }

    }
})

app.controller('PollingCtrl', function($scope, $http, $timeout) {

  var loadTime = 10000, //Load the data every second
    loadPromise; //Pointer to the promise created by the Angular $timeout service

  var getData = function() {
    $http.get('http://127.0.0.1/keepalive/' + Date.now())

    .then(function(res) {
      nextLoad();
    })
  };

  var cancelNextLoad = function() {
    $timeout.cancel(loadPromise);
  };

  var nextLoad = function(mill) {
    mill = mill || loadTime;
    //Always make sure the last timeout is cleared before starting a new one
    cancelNextLoad();
    loadPromise = $timeout(getData, mill);
  };

  //Start polling the data from the server
  getData();
  //Always clear the timeout when the view is destroyed, otherwise it will keep polling and leak memory
  $scope.$on('$destroy', function() {
    cancelNextLoad();
  });

});

app.filter("arrayNormalize", function(){

    return function(arr) {
        if (arr === null) {
            return [];
        }
        if(typeof arr === "object") {
            var arr_copy = []
            for(var i = 0; i < arr.length; i++) {
                arr_copy.push(arr[i].replace(/[\\/]+/g,"/"))
            }

            return arr_copy;
        }

        return arr;
    }

});

app.filter("pathify", function(){
    return function(arr) {
        var path = "";

        if (arr !== null) {
            path = arr.join("/")
        }

        return path
    }

});

app.directive('ruleObject', function() {
    return {
        restrict: 'E',
        scope: {
            object: '=obj'
        },
        templateUrl: '/views/rule.html'
    }

})

app.directive('rule', function() {
    //Note controller here and controllerAs can just be any function and the effect remains the same.
    //Primary and secondary directives not responding to ruleCtrlSimp.<some_func> calls for some reason
    //so resorting to a hacky way of accessing parent scope.
    return {
        restrict: 'E',
        scope: {
            ctrl: '='
        },
//        controller: ['$controller', '$scope', function($controller, $scope) {
//          var controller = $controller("RuleControllerSimp", {$scope: $scope});
//          return controller;
//        }],
//        controllerAs: "ruleCtrlSimp",
        controller: function($scope) {
        },
        replace: true,
        transclude: true,
        template: '<div ng-transclude></div>',
    }
})

app.directive('primary', function() {
    return {
        require: '^^rule',
        restrict: 'E',
        scope: {
            ruleInfo: '=rule',
        },
        transclude: true,
        replace: true,
        templateUrl: 'views/primary.html',
        link: function(scope, element, attrs) {
            scope.clickFunc = function(val,fn) {
                op = scope.$parent.ruleCtrlSimp[fn]
                op(...val)
            }
        }
    };
})

app.directive('secondary', function() {
    return {
        require: '^^rule',
        restrict: 'E',
        scope: {
            ruleInfo: '=rule',
        },
        transclude: true,
        templateUrl: 'views/secondary.html',
        link: function(scope, element, attrs) {
            scope.clickFunc = function(val,fn) {
                op = scope.$parent.ruleCtrlSimp[fn]
                op(...val)
            }

        }
    }
})

app.directive('tagEditor', function(RuleService) {
    return {
        restrict: 'E',
        template: '<input type="text" class="form-control">',
        scope: {
            ruleContainer: '=',
            rulePointer: '='
        },
        link: function(scope, element, attrs) {

            scope.availableTags = ["OR", "{test1}", "{test2}"]
            scope.states = []
            scope.replay = false;

            function colorize(editor) {
                var i = 0;

                $('li', editor).each(function(){
                    if (i !== 0) {

                        var li = $(this);

                        if(li.find('.tag-editor-tag')) {
                            var found_tag = $(li.find('.tag-editor-tag'))
                            var found_delete = $(li.find('.tag-editor-delete'))

                            if (li.find('.tag-editor-tag').html() == 'OR') {
                                found_tag.addClass('green-tag');
                                found_delete.addClass('green-tag');
                            }
                            else if (li.find('.tag-editor-tag').html() !== undefined && li.find('.tag-editor-tag').html().match("^\{[a-zA-Z0-9_\s]+\}$")) {
                                found_tag.addClass('red-tag');
                                found_delete.addClass('red-tag');
                            }
                            else {
                                found_tag.removeClass('red-tag');
                                found_delete.removeClass('red-tag');
                                found_tag.removeClass('green-tag');
                                found_delete.removeClass('green-tag');
                            }

                        }
                    }
                    i++;

                });
            }

            function tagCallback(field, editor, tags) {
                if (!scope.replay) {
                    scope.states.push([scope.ruleContainer])
                    synchronizeRuleControllerModel(tags)
                }
                colorize(editor)
            }


            function synchronizeRuleControllerModel(tags) {

                scope.$apply(function() {

                    if (scope.ruleContainer !== undefined) {
                        scope.ruleContainer = tags
                    }

                })
//                var curRule = RuleService.getRuleById(attrs.id)
//
//                if (curRule !== null && curRule !== undefined) {
//                    if (scope.ruleContainer !== undefined) {
//                        RuleService.setCurrentRuleVals(scope.ruleContainer);
//                    } else {
//                        console.log("DESYNC0")
//                    }
//                }
            }

            element.tagEditor({"initialTags": scope.ruleContainer, "onChange": tagCallback, "delimiter": ";", "maxLength": 100,
            "placeholder": "Enter a word", "forceLowercase": false, "removeDuplicates": false, "animateDelete": 30,
            "autocomplete": {
                delay: 0,
                position: {collision: 'flip'},
                source: scope.availableTags,
                minLength: 0
            }});


            function removeTags() {
                var tags = element.tagEditor("getTags")[0].tags

                if (tags) {
                    for(var i = 0; i < tags.length; i++) {
                        element.tagEditor('removeTag', tags[i]);
                    }
                }
            }

            var tag_editor = element.tagEditor("getTags")[0].editor

            $(tag_editor).on('click', '*', function(e) {

                if (!scope.replay) {
                    scope.$emit("tagEditorClick", {
                        "rule_id": attrs.id,
                        "rule": scope.rulePointer
                    })
                }
            })

            //TODO: Replay actions instead of storing state. e.g action = <add, tag_val, index> or <remove, tag_val, index>

            function undo() {
                var previous_state = scope.states.pop()[0]
                synchronizeRuleControllerModel(previous_state)
                scope.replay=true
                removeTags()
                for (var i=0; i < previous_state.length; i++) {
                    element.tagEditor("addTag", previous_state[i])
                }
                scope.replay=false
            }

            $(tag_editor).keydown(function(e) {
                if (e.ctrlKey && (e.which === 66) && scope.states.length > 0) {
                    undo()
                }
            })

            $(document).keydown(function(e) {
                if (e.ctrlKey && (e.which === 66) && scope.rulePointer.Selected && scope.states.length > 0 && e.target.nodeName !== "INPUT") {
                    undo()
                }

            })

            $(document).keydown(function(e) {
                if (e.ctrlKey && (e.which === 67) && scope.rulePointer.Selected && e.target.nodeName !== "INPUT") {
                    console.log(attrs.id)
                    scope.$emit("ruleCopy", {
                        "rule_id": attrs.id
                    })
                }
            })

            $(document).keydown(function(e) {
                if (e.ctrlKey && (e.which === 86) && scope.rulePointer.Selected && e.target.nodeName !== "INPUT") {
                    scope.$emit("rulePaste")
                }
            })

            colorize(tag_editor)

            scope.$on("reloadTags", function(event, data) {
                if(attrs.id === data.rule.u_id) {
                    element.tagEditor("addTag", data.text)
                    tagCallback(null, element)
                }
            })

        }

    }

})
