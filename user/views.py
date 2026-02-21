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
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('index')
        else:
            messages.error(request, 'Registration failed!')
    else:
        form = UserRegisterForm()

    return render(request, 'user/register.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('index')
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_redirect(request):
    """
    Redirects users based on their role after login.
    Merchants go to 'My Items', Students go to the 'Marketplace'.
    """
    # Check if a profile exists; if not, you might need to create one or handle the error
    try:
        role = request.user.profile.role
    except AttributeError:
        # Default fallback if no profile exists
        return redirect('item:item_list')

    if role == 'merchant':
        # Merchants manage their listings [cite: 172]
        return redirect('item:my_item')
    else:
        # Students browse the marketplace [cite: 168, 182]
        return redirect('item:item_list')