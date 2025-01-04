from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('about/', views.About, name='about'),
    path('contact/', views.Contact, name='contact'),
    path('menu/', views.menu, name='menu'),
    path('search/', views.search_view, name='search'),
    path('checkout/', views.checkout, name='checkout'),
    path('profile/', views.profile, name='profile'),
    path('payment_success/', views.payment_success, name='payment_success'),
]