from django.shortcuts import render, redirect
from users.forms import UserRegistrationForm, ProfileUpdateForm, UserUpdateForm
from django.contrib.auth import authenticate, login
from django.contrib import messages


def sign_up(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            form.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(
                request, message=f"Your Profile has been created {username}")
            return redirect('post:list')
    form = UserRegistrationForm()
    return render(request, template_name='users/registrartion.html', context={'form': form})


def update_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(
                request, f'Your account has been updated sucessfulluy')
            return redirect('update_profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, template_name='users/profile.html', context={'u_form': u_form, 'p_form': p_form})
