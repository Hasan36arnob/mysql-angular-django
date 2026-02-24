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
  $scope.startEdit = function(item) {
    item.editing = true;
    item.editName = item.name;
    item.editDescription = item.description;
  };
  $scope.cancelEdit = function(item) {
    item.editing = false;
  };
  $scope.saveEdit = function(item) {
    if (!item.editName || !item.editDescription) {
      $scope.error = 'Please fill in both name and description';
      return;
    }
    $http.put(API_BASE + '/items/' + item.id + '/', {
      name: item.editName,
      description: item.editDescription
    }).then(function(response) {
      item.name = response.data.name;
      item.description = response.data.description;
      item.editing = false;
      $scope.error = '';
    }).catch(function() {
      $scope.error = 'Error saving item';
    });
  };
  $scope.deleteItem = function(item) {
    $http.delete(API_BASE + '/items/' + item.id + '/delete/').then(function() {
      $scope.items = $scope.items.filter(function(i) { return i.id !== item.id; });
      $scope.error = '';
    }).catch(function() {
      $scope.error = 'Error deleting item';
    });
  };
  loadItems();
}]);
