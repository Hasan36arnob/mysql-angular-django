var app = angular.module('myApp', []);
var API_BASE = window.API_BASE || '/api';
app.controller('MainController', ['$scope', '$http', function($scope, $http) {
  $scope.items = [];
  $scope.newItem = { name: '', description: '' };
  $scope.error = '';
  function loadItems() {
    $http.get(API_BASE + '/items/').then(function(response) {
      $scope.items = response.data;
      $scope.error = '';
    }).catch(function() {
      $scope.error = 'Error loading items';
    });
  }
  $scope.addItem = function() {
    if (!$scope.newItem.name || !$scope.newItem.description) {
      $scope.error = 'Please fill in both name and description';
      return;
    }
    $http.post(API_BASE + '/items/create/', $scope.newItem).then(function(response) {
      $scope.items.push(response.data);
      $scope.newItem = { name: '', description: '' };
      $scope.error = '';
    }).catch(function() {
      $scope.error = 'Error adding item';
    });
  };
  loadItems();
}]);
