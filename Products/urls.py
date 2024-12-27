from django.urls import path
from .import views

urlpatterns = [
    path('',views.Home,name='home'),
    path('about/',views.About,name='about'),
    path('contact/',views.Contact,name='contact'),
    path('menu/',views.menu,name='menu'),
    path('offer/',views.Ouroffer,name='offer'),
    path('search/',views.search_view,name='search'),
]
