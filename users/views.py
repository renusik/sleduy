from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Создан аккаунт для пользователя {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', { 'form': form })


@login_required
def profile(request):
    if request.method == 'POST':
        userForm = UserUpdateForm(request.POST, instance=request.user)
        profileForm = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if userForm.is_valid() and profileForm.is_valid():
            userForm.save()
            profileForm.save()
            messages.success(request, f'Ваш профиль успешно обновлен.')
            return redirect('profile')

    else:
        userForm = UserUpdateForm(instance=request.user)
        profileForm = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {
            'u_form': userForm,
            'p_form': profileForm
        }
    )
