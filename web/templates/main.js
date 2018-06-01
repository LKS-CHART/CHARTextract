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
    })
}])

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

app.directive("tree", function(RecursionHelper, LoaderService, $http) {
    return {
        restrict: "E",
        scope: {
            node: "=node",
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