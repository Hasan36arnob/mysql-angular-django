var app = angular.module('myApp', []);
//ekke
// efob fhiei
app.controller('MainController', ['$scope', '$http', function($scope, $http) {
    // --- State ---
    $scope.view = 'store'; // store, product, cart, orders, login, register, wishlist
    $scope.me = null;
    $scope.products = [];
    $scope.categories = [];
    $scope.cart = [];
    $scope.orders = [];
    $scope.wishlist = [];
    $scope.selectedProduct = null;
    $scope.filters = { q: '', category: '' };
    $scope.auth = { username: '', password: '', email: '' };
    $scope.message = '';
    $scope.error = '';

    // --- Helpers ---
    function api(method, url, data) {
        $scope.message = '';
        $scope.error = '';
        return $http({ method: method, url: '/api' + url, data: data })
            .then(function(res) { return res.data; })
            .catch(function(err) {
                $scope.error = (err.data && err.data.error) ? err.data.error : 'Something went wrong';
                throw err;
            });
    }

    $scope.setView = function(v) {
        $scope.view = v;
        window.scrollTo(0, 0);
        if (v === 'store') $scope.loadProducts();
        if (v === 'cart') $scope.loadCart();
        if (v === 'orders') $scope.loadOrders();
    };

    $scope.toggleSidebar = function() {
        // Simple placeholder for mega-menu logic
        $scope.message = 'All Departments Menu Clicked';
    };

    // --- Wishlist ---
    $scope.toggleWishlist = function(product) {
        product.isWishlisted = !product.isWishlisted;
        if (product.isWishlisted) {
            $scope.message = 'Added to Wishlist';
        } else {
            $scope.message = 'Removed from Wishlist';
        }
    };
// fekjfles 
//jfiejfilj 
//fejifj


    // --- Auth ---
    $scope.login = function() {
        api('POST', '/auth/login/', $scope.auth).then(function(user) {
            $scope.me = user;
            $scope.auth = { username: '', password: '', email: '' };
            $scope.setView('store');
        });
    };

    $scope.register = function() {
        api('POST', '/auth/register/', $scope.auth).then(function(user) {
            $scope.me = user;
            $scope.auth = { username: '', password: '', email: '' };
            $scope.setView('store');
        });
    };

    $scope.logout = function() {
        api('POST', '/auth/logout/').then(function() {
            $scope.me = null;
            $scope.setView('store');
        });
    };

    function checkAuth() {
        api('GET', '/auth/me/').then(function(user) { $scope.me = user; }).catch(function(){});
    }

    // --- Store ---
    $scope.loadProducts = function() {
        var params = '?q=' + ($scope.filters.q || '') + '&category=' + ($scope.filters.category || '');
        api('GET', '/products/' + params).then(function(data) { $scope.products = data; });
    };

    $scope.loadCategories = function() {
        api('GET', '/categories/').then(function(data) { 
            $scope.categories = data; 
        });
    };

    $scope.viewProduct = function(slug) {
        api('GET', '/products/' + slug + '/').then(function(data) {
            $scope.selectedProduct = data;
            $scope.setView('product');
        });
    };

    // --- Cart ---
    $scope.loadCart = function() {
        api('GET', '/cart/').then(function(data) { $scope.cart = data; });
    };

    $scope.addToCart = function(productId, qty) {
        if (!$scope.me) { $scope.setView('login'); return; }
        api('POST', '/cart/', { product_id: productId, quantity: qty || 1 }).then(function() {
            $scope.message = 'Added to cart!';
        });
    };

    $scope.removeFromCart = function(itemId) {
        api('DELETE', '/cart/remove/' + itemId + '/').then(function() { $scope.loadCart(); });
    };

    $scope.cartTotal = function() {
        return $scope.cart.reduce(function(sum, item) {
            return sum + (parseFloat(item.price) * item.quantity);
        }, 0);
    };

    // --- Orders ---
    $scope.checkout = function() {
        api('POST', '/checkout/').then(function(res) {
            $scope.message = 'Order placed successfully! Order ID: ' + res.order_id;
            $scope.cart = [];
            $scope.setView('orders');
        });
    };

    $scope.loadOrders = function() {
        api('GET', '/orders/').then(function(data) { $scope.orders = data; });
    };

    // --- Init ---
    checkAuth();
    $scope.loadCategories();
    $scope.loadProducts();
}]);
