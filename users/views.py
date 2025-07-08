from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Login view
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect(f'/chat/{user.username}/')  # ✅ dynamic redirect
        else:
            messages.error(request, 'Invalid username or password. Please try again.')

    if request.user.is_authenticated:
        return redirect(f'/chat/{request.user.username}/')  # ✅ dynamic redirect

    return render(request, 'login.html')


# Logout view
@login_required
def logout_page(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('/')


# Signup view
def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password1 != confirm_password:
            messages.error(request, 'Passwords do not match. Please try again.')
            return render(request, 'signup.html')

        # Check if username is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken. Please choose another one.')
            return render(request, 'signup.html')

        # Check if email is already in use
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use. Please try another one.')
            return render(request, 'signup.html')

        # Create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        user.save()
        messages.success(request, 'Signup successful! You can now log in.')
        return redirect('login')

    if request.user.is_authenticated:
        return redirect(f'/chat/{request.user.username}/')  # ✅ fixed dynamic redirect

    return render(request, 'signup.html')
