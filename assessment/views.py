from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.generic import ListView, TemplateView, CreateView, UpdateView

from assessment.forms import CreateAssessmentForm
from assessment.models import PunishmentReward, ScaleAnswer, Assessment, Season
from authentication.models import Employee, User
from . import forms


class AssessedsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    context_object_name = 'answers'
    template_name = 'assessment/assessment-list.html'

    def test_func(self):
        if self.request.user.is_employee():
            return True
        return False

    def get_queryset(self):
        assessor = self.request.user.get_employee()
        answers = assessor.get_unresolved_answers()
        return answers

    def get_context_data(self, **kwargs):
        context = super(AssessedsListView, self).get_context_data(**kwargs)
        context['not_found'] = False
        if self.get_queryset() is None or len(self.get_queryset()) < 1:
            context['not_found'] = True
        return context


class AddScaleView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = "assessment/add-scale.html"
    form_class = forms.AddScaleForm

    def test_func(self):
        if self.request.user.is_admin():
            return True
        return False

    def get_success_url(self):
        return reverse('dashboard')


class EmployeesListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "assessment/employee-list.html"
    model = Employee
    context_object_name = "employees"

    def test_func(self):
        if self.request.user.is_admin():
            return True
        return False




class ShowEmployeeView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    model = User
    template_name = 'assessment/show-employee.html'

    def test_func(self):
        if self.request.user.is_admin():
            if self.request.user.id != self.kwargs.get("pk"):
                return True
        if self.request.user.is_employee():
            if self.request.user.id == self.kwargs.get("pk"):
                return True
        return False

    def get_context_data(self, **kwargs):
        context = super(ShowEmployeeView, self).get_context_data(**kwargs)
        user = User.objects.get_by_id(self.kwargs.get("pk"))  # TODO handle None
        not_found_user = False
        assessment = None
        employee = None
        if user:
            employee = user.get_employee()
            print(user.get_job())
            if employee:
                assessment = employee.get_current_assessment()
        else:
            not_found_user = True


        context['not_found_user'] = not_found_user
        context['user'] = user
        context['employee'] = employee
        context['viewer'] = self.request.user
        context['assessment'] = assessment
        return context


class CreateAssessment(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Assessment
    template_name = 'assessment/add-assessment.html'
    form_class = CreateAssessmentForm
    user = None

    def get_form_kwargs(self):
        kwargs = super(CreateAssessment, self).get_form_kwargs()
        self.user = User.objects.get_by_id(self.kwargs.get("pk"))
        kwargs.update({'user': self.user})
        return kwargs

    def test_func(self):
        if self.request.user.is_admin():
            return True
        return False

    def get_success_url(self):
        return reverse('show_my_details')


class DoAssessmentView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ScaleAnswer
    form_class = forms.ScaleAnswerForm
    template_name = 'assessment/assess.html'

    def test_func(self):
        if self.request.user.is_employee():
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super(DoAssessmentView, self).get_context_data(**kwargs)
        sa = self.get_object()
        context['assessed'] = sa.get_assessment().get_assessed().get_user()
        context['scale'] = sa.scale
        return context

    def get_success_url(self):
        return reverse('assessment_list')


class SetPunishmentRewardView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = PunishmentReward
    form_class = forms.PunishmentRewardForm
    template_name = "assessment/punishment-reward.html"

    def test_func(self):
        if self.request.user.is_admin():
            return True
        return False

    def get_success_url(self):
        return reverse('employee_list')


class AddSeasonView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Season
    form_class = forms.AddSeasonForm
    template_name = 'assessment/add-season.html'

    def test_func(self):
        if self.request.user.is_admin():
            return True
        return False

    def get_success_url(self):
        return reverse('dashboard')
