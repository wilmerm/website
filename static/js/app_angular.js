


	// --------------------------------------------
    // Angular JS
    // App en la plantilla base.html
	// --------------------------------------------

	var searchModulosBaseURL = "/json/modulo/html/list/"
	var app = angular.module("myApp", []);

	app.controller("myCtrl", function($scope, $http) {

		// Busca módulos.
		$scope.onSearchModulos = function() {
			kw = "?q=" + $scope.searchModulosInput + "&outType=objects" + "&limit=10";
			$http.get(searchModulosBaseURL + kw).then(function(res) {
				$scope.searchModulosDataJSON = res.data.data;
			});
		}
	});