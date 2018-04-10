app.controller('ErrorController', function($scope, DataService){

    var myDataPromise = DataService.getData()
    $scope.selected = null;
    $scope.selected_id = null;
    $scope.overview = true;
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

})