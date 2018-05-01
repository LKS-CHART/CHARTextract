app = angular.module('app', ['ngRoute']).config(['$routeProvider', function($routeProvider) {
    $routeProvider.
    when('/overview', {
        templateUrl: 'overview.html',
    }).
    when('/view', {
        templateUrl: 'view.html',
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
