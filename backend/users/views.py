from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import RegistrationForm, LoginForm, UserUpdateForm, ProfileUpdateForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Save the user data (User model)
            user = form.save(commit=False)  # Don't save yet
            user.set_password(form.cleaned_data['password1'])  # Set the password using the form data
            user.save()

            # Create a Profile instance for the new user
            profile = Profile(
                user=user,
                date_of_birth=form.cleaned_data.get('date_of_birth'),
                address=form.cleaned_data.get('address'),
                city=form.cleaned_data.get('city'),
                country=form.cleaned_data.get('country'),
                image=form.cleaned_data.get('image')
            )
            profile.save()

            # Log the user in
            login(request, user)
            
            messages.success(request, f'Account created for {user.username}!')
            return redirect('reviews:home')
    else:
        form = RegistrationForm()

    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('reviews:home')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form, 'title': 'Login'})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('reviews:home')

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('reviews:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'title': 'My Profile'
    }
    return render(request, 'users/profile.html', context)

