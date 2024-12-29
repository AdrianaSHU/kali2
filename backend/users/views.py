from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import RegistrationForm, LoginForm, UserUpdateForm, ProfileUpdateForm, PasswordChangeFormCustom



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Save the user data (User model)
            user = form.save(commit=False)  # Don't save the user yet
            user.set_password(form.cleaned_data['password1'])  # Set the password from the form
            user.save()

            # Save the profile data
            profile = Profile(user=user)
            profile.date_of_birth = form.cleaned_data['date_of_birth']
            profile.address = form.cleaned_data['address']
            profile.city = form.cleaned_data['city']
            profile.country = form.cleaned_data['country']
            if form.cleaned_data['image']:
                profile.image = form.cleaned_data['image']
            profile.save()

            # Log the user in
            login(request, user)
            
            messages.success(request, f'Account created for {user.username}!')
            return redirect('reviews:home')  # Redirect to homepage or user dashboard
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
    user = request.user

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=user.profile)
        password_form = PasswordChangeFormCustom(request.POST)

        if 'update_profile' in request.POST:
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, 'Your profile has been updated!')
        elif 'change_password' in request.POST:
            if password_form.is_valid():
                current_password = password_form.cleaned_data['current_password']
                new_password = password_form.cleaned_data['new_password']
                if not user.check_password(current_password):
                    messages.error(request, "Your current password is incorrect.")
                else:
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)  # To prevent logging out after password change
                    messages.success(request, "Your password has been updated!")
                    return redirect('reviews:profile')  # Redirect to avoid re-posting data on refresh
            else:
                for field, errors in password_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.capitalize()}: {error}")
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=user.profile)
        password_form = PasswordChangeFormCustom()

    return render(request, 'users/profile.html', {
        'u_form': u_form,
        'p_form': p_form,
        'password_form': password_form,
        'title': 'My Profile',
        'profile': user.profile
    })