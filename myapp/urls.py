from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    # Auth
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/me/', views.me_view, name='me'),
    
    # Storefront
    path('products/', views.product_list, name='product_list'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('categories/', views.category_list, name='category_list'),
    
    # Cart
    path('cart/', views.cart_view, name='cart'),
    path('cart/remove/<int:item_id>/', views.cart_remove, name='cart_remove'),
    
    # Orders
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.my_orders, name='my_orders'),
]
