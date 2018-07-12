from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from . import forms
from .models import User, Unit


# TODO set permissions on every class
class LoginView(auth_views.LoginView):
    template_name = 'authentication/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        if self.request.user.is_employee():
            return reverse('show_my_details')
        else:
            return reverse('employee_list')


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    template_name = 'authentication/logout.html'


class AddEmployeeView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = User
    template_name = 'authentication/add-employee.html'
    form_class = forms.AddEmployeeForm

    def test_func(self):
        if self.request.user.is_admin():
            return True
        return False

    def get_success_url(self):
        return reverse('employee_list')


class UpdateUsernameOrPasswordView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = forms.ChangeUsernameOrPasswordForm
    template_name_suffix = '_update'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('login')


class AddUnitView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Unit
    form_class = forms.AddUnitForm
    template_name = 'authentication/add-unit.html'

    def test_func(self):
        if self.request.user.is_admin():
            return True
        return False

    def get_success_url(self):
        return reverse('dashboard')


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'authentication/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        context['is_admin'] = self.request.user.is_admin()
        context['is_employee'] = self.request.user.is_employee()
        return context
