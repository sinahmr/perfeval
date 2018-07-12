from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.generic import ListView, TemplateView, CreateView, UpdateView

from assessment.forms import CreateAssessmentForm
from assessment.models import Scale, PunishmentReward, ScaleAnswer, Assessment, Season
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

    def test_func(self):
        if self.request.user.is_admin():
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super(EmployeesListView, self).get_context_data(**kwargs)
        employees = Employee.objects.all()
        for emp in employees:
            emp.has_assessor = False
            emp.assessment_done = False
            assessment = emp.assessments_as_assessed.filter(season=Season.objects.get_current_season()).first()
            if assessment:
                emp.has_assessor = True
                if assessment.is_done():
                    emp.assessment_done = True

        context['employees'] = employees
        return context


class ShowEmployeeView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    model = User
    template_name = 'assessment/show-employee.html'

    def test_func(self):
        if self.request.user.is_admin():
            return True
        if self.request.user.is_employee():
            if self.request.user.id == self.kwargs.get("pk"):
                return True
        return False

    def get_context_data(self, **kwargs):
        context = super(ShowEmployeeView, self).get_context_data(**kwargs)
        user = User.objects.get_by_id(self.kwargs.get("pk"))  # TODO handle None
        not_found_user = False
        has_assessment = True
        done_assessment = True
        if user:
            if user.is_employee():
                assessment = user.get_employee().assessments_as_assessed.last()
        else:
            not_found_user = True

        if assessment is None:
            has_assessment = False
            done_assessment = False
        if has_assessment:
            done_assessment = assessment.is_done()

        context['done_assessment'] = done_assessment
        context['not_found_user'] = not_found_user
        context['user'] = user
        context['viewer'] = self.request.user
        context['assessment'] = assessment
        context['has_assessment'] = has_assessment
        return context


class ShowMyDetailsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    model = Employee
    template_name = 'assessment/show-employee.html'

    def test_func(self):
        if self.request.user.is_employee():
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super(ShowMyDetailsView, self).get_context_data(**kwargs)
        user = self.request.user
        assessment = user.get_employee().assessments_as_assessed.last()
        has_assessment = True
        done_assessment = True
        if assessment is None:
            has_assessment = False
            done_assessment = False
        if has_assessment:
            done_assessment = assessment.is_done()

        context['user'] = user
        context['assessment'] = assessment
        context['has_assessment'] = has_assessment
        context['done_assessment'] = done_assessment
        return context


class CreateAssesment(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Assessment
    template_name = 'assessment/add-assessment.html'
    form_class = CreateAssessmentForm
    user = None

    def get_form_kwargs(self):
        kwargs = super(CreateAssesment, self).get_form_kwargs()
        self.user = User.objects.get_by_id(self.kwargs.get("pk"))
        kwargs.update({'user': self.user})
        return kwargs

    def test_func(self):
        if self.request.user.is_admin():
            return True
        return False

    def get_success_url(self):
        return reverse('show_my_details')


class PunishmentRewardListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "assessment/scale-list.html"
    model = PunishmentReward

    def test_func(self):
        return True


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
        context['assessed'] = sa.assessment.assessed.get_user()
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
