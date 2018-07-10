from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.generic import ListView, TemplateView, CreateView, FormView, UpdateView

from assessment.models import Scale, PunishmentReward, ScaleAnswer, Assessment
from authentication.forms import CreateAssessmentForm
from authentication.models import Employee, User , Unit
from . import forms


class AssessedsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    context_object_name = 'assesseds'
    template_name = 'assessment/assessment-list.html'

    def test_func(self):
        if self.request.user.is_employee():
            return True
        return False

    def get_queryset(self):
        assessor = self.request.user.get_employee()
        return assessor.get_assesseds()

    def get_context_data(self, **kwargs):
        context = super(AssessedsListView, self).get_context_data(**kwargs)
        context['not_found'] = False
        if self.get_queryset() is None or len(self.get_queryset()) < 1:
            context['not_found'] = True
        return context


class AddScaleView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = "assessment/add-scale.html"
    form_class = forms.AddScaleForm

    def test_func(self):
        return True


class ScaleListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "assessment/scale-list.html"
    model = Scale

    def test_func(self):
        return True


class EmployeesListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "assessment/employee-list.html"
    model = Employee

    def test_func(self):
        return True


class ShowEmployeeView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    model = User
    template_name = 'assessment/show-employee.html'

    def test_func(self):
        if self.request.user.is_admin():
            return True
        if self.request.user.is_employee():
            print("Hello")
            if self.request.user.id == self.kwargs.get("pk"):
                print(self.kwargs.get("pk"))
                return True
        return False

    def get_context_data(self, **kwargs):
        context = super(ShowEmployeeView, self).get_context_data(**kwargs)
        user = User.objects.get_by_id(self.kwargs.get("pk"))
        if user.is_employee():
            assessments = user.get_employee().assessments_as_assessed.all()
        else:
            assessments = []
        has_assessment = True
        if assessments is None or len(assessments) < 1:
            has_assessment = False
        for assessment in assessments:
            pass
            # TODO SET has_assessment
            #   has_assessment = False
        context['create_assessment_link'] = '/assessment/create/'+str(self.kwargs.get("pk"))+'/'
        context['user'] = user
        context['assessments'] = assessments
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
        employee = self.request.user.get_employee()
        assessments = employee.assessments_as_assessed.all()
        has_assessment = True
        if assessments is None or len(assessments) < 1:
            has_assessment = False
        for assessment in assessments:
             pass
             # TODO SET has_assessment
             #   has_assessment = False
        context['employee'] = employee
        context['assessments'] = assessments
        context['has_assessment'] = has_assessment
        return context


class CreateAssesment(LoginRequiredMixin, UserPassesTestMixin,CreateView):
    model = Assessment
    template_name = 'assessment/add-assessment.html'
    form_class = CreateAssessmentForm

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


class SetPunishmentRewardView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = "assessment/scale-list.html"
    model = PunishmentReward

    def test_func(self):
        return True
