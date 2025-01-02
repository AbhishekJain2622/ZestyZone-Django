from . import views
from django.urls import path

urlpatterns = [
    path('', views.Home, name='home'),
    path('about/', views.About, name='about'),
    path('contact/', views.Contact, name='contact'),
    path('menu/', views.menu, name='menu'),
    path('search/', views.search_view, name='search'),
    path('checkout/', views.checkout, name='checkout'),
    path('profile/', views.profile, name='profile'),
    # path('admin2/', views.admin_view, name='admin_dashboard'),
    # path('admin2/orders/', views.admin_orders, name='admin_orders'),
    # path('admin2/products/', views.admin_products, name='admin_products'),
    # path('admin2/users/', views.admin_users, name='admin_users'),
]