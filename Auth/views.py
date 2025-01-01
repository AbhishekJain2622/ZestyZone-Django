import re
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages

# Helper function to send email
def send_email(subject, message, recipient_list):
    from_email = 'your-email@gmail.com'  # Replace with your email
    send_mail(subject, message, from_email, recipient_list)

# Password validation
def is_valid_password(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "Password must include at least one special character."
    if not re.search(r"\d", password):
        return "Password must include at least one number."
    return None

# Signup functionality
def Signup(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('pass1')
        confirm_password = request.POST.get('pass2')

        # Validate password
        password_error = is_valid_password(password)
        if password_error:
            messages.error(request, password_error)
            return redirect('/auth/signup/')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('/auth/signup/')

        # Check if the email is already taken
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('/auth/signup/')

        # Create a new user
        user = User.objects.create_user(username=email, email=email, password=password)
        user.is_active = False  # Deactivate user until email is verified
        user.save()

        # Generate token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        verification_link = f"http://{get_current_site(request).domain}/auth/verify-email/{uid}/{token}/"

        # Send verification email
        send_email("Verify your email", f"Click the link to verify your email: {verification_link}", [email])

        messages.success(request, "A verification link has been sent to your email.")
        return redirect('/auth/signup/')

    return render(request, 'authentication/signup.html')

# Email verification
def verify_email(request, uidb64, token):
    try:
        user_id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=user_id)
        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Email verified successfully. You can now log in.")
            return redirect('/auth/login/')
        else:
            messages.error(request, "Invalid or expired verification link.")
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, "Invalid verification link.")
    return redirect('/auth/signup/')

# Login functionality
def Login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('pass1')
        myuser = authenticate(username=email, password=password)

        if myuser is not None:
            login(request, myuser)
            messages.success(request, "Login Success")
            return redirect('/')
        else:
            messages.error(request, "Invalid Credentials")
    return render(request, 'authentication/login.html')

# Logout functionality
def Logout(request):
    logout(request)
    messages.success(request, 'Logout successful')
    return redirect('/auth/login/')
def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "No account found with this email.")
            return redirect('/auth/forgot-password/')

        # Generate password reset token and link
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = f"http://{request.get_host()}/auth/reset-password/{uid}/{token}/"

        # Send email
        send_mail(
            "Reset Your Password",
            f"Click the link to reset your password: {reset_link}",
            "your-email@example.com",  # Replace with your email
            [email],
            fail_silently=False,
        )
        messages.success(request, "A password reset link has been sent to your email.")
        return redirect('/auth/login/')

    return render(request, 'authentication/forgot_password.html')

# Reset password functionality
def reset_password(request, uidb64, token):
    if request.method == "POST":
        password = request.POST.get('pass1')
        confirm_password = request.POST.get('pass2')

        # Validate password
        password_error = is_valid_password(password)
        if password_error:
            messages.error(request, password_error)
            return redirect(request.path)

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect(request.path)

        # Decode UID and validate token
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            if default_token_generator.check_token(user, token):
                user.set_password(password)
                user.save()
                messages.success(request, "Password reset successfully. You can now log in.")
                return redirect('/auth/login/')
            else:
                messages.error(request, "Invalid or expired reset link.")
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            messages.error(request, "Invalid reset link.")
        return redirect('/auth/forgot-password/')

    return render(request, 'authentication/reset_password.html')
