from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .exceptions import FailedLogin, RepetitiousUsername
from .models import User
from . import forms


def add_user(request):
    if request.method == 'POST':
        form = forms.AddEmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'ثبت شد')
            form = forms.AddEmployeeForm()
        else:
            messages.error(request, 'ثبت نشد')
    else:
        form = forms.AddEmployeeForm()

    return render(request, 'authentication/add-user.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            try:
                User.login(request, username, password)
                messages.success(request, 'با موفقیت وارد شدید')
                return redirect('employee_list')  # TODO Change
            except FailedLogin:
                messages.error(request, 'عدم تطابق نام کاربری با گذرواژه')
    else:
        form = forms.LoginForm()

    return render(request, 'authentication/login.html', {'form': form})


@login_required
def change_username_or_password(request):
    if request.method == 'POST':
        form = forms.ChangeUsernameOrPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            try:
                request.user.change_username_and_password(username, password)
                messages.success(request, 'انجام شد')
                return redirect('login')
            except RepetitiousUsername:
                messages.error(request, 'نام کاربری تکراری است')
    else:
        form = forms.ChangeUsernameOrPasswordForm()

    return render(request, 'authentication/change-username-or-password.html', {'form': form})


def delete_user(request, user_id):  # TODO Delete this
    user = User.get_user_by_id(user_id)
    if user:
        user.delete()
        return HttpResponse('انجام شد')
    return HttpResponse('کاربر یافت نشد')
