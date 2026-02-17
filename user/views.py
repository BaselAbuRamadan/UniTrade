from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, UserRegisterForm


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                next_url = request.GET.get('next', '/')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password!')
    else:
        form = UserLoginForm()

    return render(request, 'user/login.html', {'form': form})


def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'The two passwords do not match!')
            return render(request, 'user/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'user/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email has already been registered!')
            return render(request, 'user/register.html')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        login(request, user)
        messages.success(request, 'Registration successful!')
        return redirect('index')

    return render(request, 'user/register.html')


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('index')
