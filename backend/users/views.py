from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import Profile
from .forms import RegistrationForm, LoginForm, UserUpdateForm, ProfileUpdateForm, PasswordChangeFormCustom



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Save the user data (User model)
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Set the password
            user.save()
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
    if not hasattr(request.user, 'profile'):
        # If profile does not exist, redirect or handle the creation
        return redirect('profile_creation_url')  # Or wherever you handle creating a profile

    if request.method == 'POST':
        # Check if it's a password change form
        password_form = PasswordChangeFormCustom(request.POST)
        
        if password_form.is_valid():
            current_password = password_form.cleaned_data['current_password']
            new_password = password_form.cleaned_data['new_password']
            user = request.user

            # Check if the current password is correct
            if not user.check_password(current_password):
                messages.error(request, "Your current password is incorrect.")
            else:
                # Set the new password
                user.set_password(new_password)
                user.save()

                # Re-login user after password change
                update_session_auth_hash(request, user)
                
                messages.success(request, "Your password has been updated!")
                return redirect('reviews:profile')  # Redirect to avoid re-posting data on refresh

        else:
            # Add specific errors from the form to the messages framework
            for field, errors in password_form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

    # Load the user update form
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)

    # Initialize the password change form (for rendering)
    password_form = PasswordChangeFormCustom()

    return render(request, 'users/profile.html', {
        'u_form': u_form,
        'p_form': p_form,
        'password_form': password_form,
        'title': 'My Profile',
        'profile': request.user.profile  # Safe to access because we checked existence above
    })
