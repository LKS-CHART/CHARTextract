app = angular.module('app', ['ngRoute']).config(['$routeProvider', function($routeProvider) {
    $routeProvider.
    when('/overview', {
        templateUrl: 'overview.html',
    }).
    when('/view', {
        templateUrl: 'view.html',
    })
}])