from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST'and 'update' in request.POST:
        u_form = UserUpdateForm(request.POST, instance=request.user)

        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    elif request.method == 'POST' and 'change_password' in request.POST:
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password has been updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Smth went wrong, please try again')

    form = PasswordChangeForm(request.user)
    u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form,
        'form': form,
    }
    return render(request, 'users/profile.html', context)

@login_required
def account(request):
    if request.method == 'POST'and 'update' in request.POST:
        u_form = UserUpdateForm(request.POST, instance=request.user)

        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    elif request.method == 'POST' and 'change_password' in request.POST:
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password has been updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Smth went wrong, please try again')

    form = PasswordChangeForm(request.user)
    u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form,
        'form': form,
    }
    return render(request, 'users/account.html', context)
