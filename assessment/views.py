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
        return self.request.user.has_permission("R", "A")#read #assessment

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
        return self.request.user.has_permission("C", "S")#create #scale

    def get_success_url(self):
        return reverse('dashboard')


class EmployeesListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "assessment/employee-list.html"
    model = Employee
    context_object_name = "employees"

    def test_func(self):
        return self.request.user.has_permission("R", "E") #read #employee


class ShowEmployeeView(LoginRequiredMixin, TemplateView):
    model = User
    template_name = 'assessment/show-employee.html'

    def get_context_data(self, **kwargs):
        context = super(ShowEmployeeView, self).get_context_data(**kwargs)
        user = User.objects.get_by_id(self.kwargs.get("pk"))  # TODO handle None
        return self.request.user.show_employee_page(self, user, context)



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
        return self.request.user.has_permission("C", "A")  # create #Assessment

    def get_success_url(self):
        return reverse('dashboard')


class DoAssessmentView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ScaleAnswer
    form_class = forms.ScaleAnswerForm
    template_name = 'assessment/assess.html'

    def test_func(self):
        return self.request.user.has_permission("E", "A")  #edit #Assessment

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
        return self.request.user.has_permission("E", "P")  # create #Assessment

    def get_success_url(self):
        return reverse('employee_list')


class AddSeasonView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Season
    form_class = forms.AddSeasonForm
    template_name = 'assessment/add-season.html'

    def test_func(self):
        return self.request.user.has_permission("C", "N")  #createe #Season

    def get_success_url(self):
        return reverse('dashboard')
