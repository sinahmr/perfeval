from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import reverse
from django.views.generic.edit import CreateView, UpdateView

from . import forms
from .models import Employee


# TODO set permissions on every class
class LoginView(auth_views.LoginView):
    template_name = 'authentication/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        if self.request.user.is_employee():
            return reverse('assessment_list')
        else:
            return reverse('show_my_details')


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    template_name = 'authentication/logout.html'


class AddEmployeeView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Employee
    template_name_suffix = '_add'
    form_class = forms.AddEmployeeForm

    def test_func(self):
        if self.request.user.is_admin():
            return True
        return False

    def get_success_url(self):
        return reverse('employee_list')


class UpdateUsernameOrPasswordViewForEmployee(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Employee
    form_class = forms.ChangeUsernameOrPasswordForm
    template_name_suffix = '_update'

    def test_func(self):
        if self.request.user.is_employee():
            return True
        return False

    def get_object(self):
        return self.request.user.employee

    def get_success_url(self):
        return reverse('login')
