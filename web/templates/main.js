app = angular.module('app', ['ngRoute']).config(['$routeProvider', function($routeProvider) {
    $routeProvider.
    when('/view', {
        templateUrl: 'view.html',
        controller: 'ErrorController',
        controllerAs: 'errorCtrl',
    }).
    when('/overview', {
        templateUrl: 'overview.html',
        controller: 'ErrorController',
        controllerAs: 'errorCtrl',
    }).
    when('/settings', {
        templateUrl: 'settings.html',
        controller: 'ErrorController',
        controllerAs: 'errorCtrl',
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