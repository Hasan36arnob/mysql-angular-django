var app = angular.module('myApp', []);
var API_BASE = window.API_BASE || '/api';
app.controller('MainController', ['$scope', '$http', function($scope, $http) {
  // session
  $scope.me = null;
  $scope.auth = { username: '', password: '', error: '' };
  // projects
  $scope.projects = [];
  $scope.projectQuery = { q: '', limit: 20, offset: 0 };
  $scope.newProject = { name: '', description: '' };
  $scope.currentProject = null;
  // tasks
  $scope.tasks = [];
  $scope.taskQuery = { q: '', status: '', priority: '', limit: 20, offset: 0 };
  $scope.newTask = { title: '', description: '', priority: 'medium', status: 'todo', tagsText: '' };
  // comments
  $scope.comments = [];
  $scope.newComment = { body: '' };
  // ui state
  $scope.error = '';
  $scope.message = '';
  $scope.loading = false;
  $scope.saving = false;

  function get(url, params) { return $http.get(API_BASE + url, { params: params || {} }); }
  function post(url, body) { return $http.post(API_BASE + url, body || {}); }
  function put(url, body) { return $http.put(API_BASE + url, body || {}); }
  function del(url) { return $http.delete(API_BASE + url); }

  // session
  function loadMe() {
    return get('/auth/me/').then(function(res) { $scope.me = res.data.user; });
  }
  $scope.login = function() {
    $scope.auth.error = '';
    post('/auth/login/', { username: $scope.auth.username, password: $scope.auth.password })
      .then(function(res) { $scope.me = res.data.user; $scope.message = 'Logged in'; })
      .catch(function(err) { $scope.auth.error = (err.data && err.data.error) || 'Login failed'; });
  };
  $scope.logout = function() {
    post('/auth/logout/').finally(function() { $scope.me = null; });
  };

  // projects
  function loadProjects() {
    $scope.loading = true;
    return get('/projects/', $scope.projectQuery).then(function(res) {
      $scope.projects = res.data.results;
      $scope.loading = false;
    }).catch(function() { $scope.loading = false; $scope.error = 'Failed to load projects'; });
  }
  $scope.createProject = function() {
    if (!$scope.newProject.name) { $scope.error = 'Project name required'; return; }
    $scope.saving = true;
    post('/projects/create/', $scope.newProject).then(function(res) {
      $scope.projects.unshift(res.data);
      $scope.newProject = { name: '', description: '' };
      $scope.message = 'Project created';
      $scope.saving = false;
    }).catch(function() { $scope.error = 'Failed to create project'; $scope.saving = false; });
  };
  $scope.selectProject = function(p) {
    $scope.currentProject = p;
    $scope.taskQuery.offset = 0;
    loadTasks();
  };

  // tasks
  function loadTasks() {
    if (!$scope.currentProject) { $scope.tasks = []; return; }
    $scope.loading = true;
    return get('/projects/' + $scope.currentProject.id + '/tasks/', $scope.taskQuery).then(function(res) {
      $scope.tasks = res.data.results;
      $scope.loading = false;
    }).catch(function() { $scope.loading = false; $scope.error = 'Failed to load tasks'; });
  }
  $scope.createTask = function() {
    if (!$scope.currentProject) return;
    if (!$scope.newTask.title) { $scope.error = 'Task title required'; return; }
    var payload = angular.copy($scope.newTask);
    payload.tags = (payload.tagsText || '').split(',').map(function(s){return s.trim();}).filter(Boolean);
    $scope.saving = true;
    post('/projects/' + $scope.currentProject.id + '/tasks/create/', payload).then(function() {
      $scope.newTask = { title: '', description: '', priority: 'medium', status: 'todo', tagsText: '' };
      $scope.message = 'Task created';
      $scope.saving = false;
      loadTasks();
    }).catch(function() { $scope.error = 'Failed to create task'; $scope.saving = false; });
  };
  $scope.updateTask = function(t, fields) {
    put('/tasks/' + t.id + '/', fields).then(function() {
      Object.assign(t, fields);
      $scope.message = 'Task updated';
    }).catch(function() { $scope.error = 'Failed to update task'; });
  };
  $scope.deleteTask = function(t) {
    del('/tasks/' + t.id + '/delete/').then(function() {
      $scope.tasks = $scope.tasks.filter(function(x){ return x.id !== t.id; });
      $scope.message = 'Task deleted';
    }).catch(function() { $scope.error = 'Failed to delete task'; });
  };
  $scope.filterTasks = function() { loadTasks(); };

  // comments
  $scope.loadComments = function(t) {
    get('/tasks/' + t.id + '/comments/').then(function(res){ t._comments = res.data; });
  };
  $scope.addComment = function(t) {
    if (!t._newBody) return;
    post('/tasks/' + t.id + '/comments/create/', { body: t._newBody, author_id: $scope.me ? $scope.me.id : null })
      .then(function() { t._newBody=''; $scope.loadComments(t); $scope.message = 'Comment added'; })
      .catch(function(){ $scope.error='Failed to add comment'; });
  };

  // initialize
  loadMe().finally(function() { loadProjects(); });
}]);
