from django.urls import path
from .import views

urlpatterns = [
    path('signup/',views.Signup,name='singup'),
    path('login/',views.Login,name='login'),
    path('logout/',views.Logout,name='logout'),
    # Email Verification (handles verification link after user signs up)
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),  # Forgot password
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password'), # Reset passwor
    # # Email verification URL
    # path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),

    # # Razorpay Payment Callback URL (replace with actual callback URL in your case)
    # path('payment/success/', views.razorpay_payment_callback, name='razorpay_payment_callback'),  # Payment success handler

]
