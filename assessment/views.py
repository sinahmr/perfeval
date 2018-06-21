from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView

from authentication.models import Employee
from . import forms


class EmployeesListView(LoginRequiredMixin, UserPassesTestMixin,ListView):
    context_object_name = 'assesseds'
    template_name = 'assessment/assessment-list.html'

    def test_func(self):
        if self.request.user.is_employee():
            return True
        return False

    def get_queryset(self):
        assessor=self.request.user.employee
        assessments = assessor.assessments_as_assessor.all()
        assesseds=[]
        for assessment in assessments:
            assesseds.append(assessment.assessed)
        return assesseds

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(EmployeesListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        not_found=False
        if self.get_queryset() is None or len(self.get_queryset()) < 1:
            not_found=True
        context['not_found'] = not_found
        return context

# def add_criterion(request):
#     if request.method == 'POST':
#         form = forms.AddCriterionForm(request.POST)
#     else:
#         form = forms.AddCriterionForm()
#
#     return render(request, 'assessment/add-criterion.html', {'form': form})
#
#
# def criterion_list(request):
#     return render(request, 'assessment/criterion-list.html', {})
#
#
def employee_list(request):
    return render(request, 'assessment/employee-list.html', {})


class ShowEmployeeView(LoginRequiredMixin, UserPassesTestMixin,TemplateView):
    model = Employee
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
        employee = Employee.objects.get_by_id(self.kwargs.get("pk"))
        if employee:
            assessments = employee.assessments_as_assessed.all()
        else:
            assessments = []
        has_assessment = True
        if assessments is None or len(assessments)<1:
            has_assessment = False
        context['employee'] = employee
        context['assessments'] = assessments
        context['has_assessment'] = has_assessment
        return context


class ShowMyDetailsView(LoginRequiredMixin, UserPassesTestMixin,TemplateView):
    model = Employee
    template_name = 'assessment/show-employee.html'

    def test_func(self):
        return True

    def get_context_data(self, **kwargs):
        context = super(ShowMyDetailsView, self).get_context_data(**kwargs)
        employee = Employee.objects.get_by_id(self.request.user.id)
        assessments = employee.assessments_as_assessed.all()
        has_assessment = True
        if assessments is None or len(assessments) < 1:
            has_assessment = False
        context['employee'] = employee
        context['assessments'] = assessments
        context['has_assessment'] = has_assessment
        return context



#
# def assessment_list(request):
#     return render(request, 'assessment/assessment-list.html', {})
#
#
# def assess(request, employee_id):
#     return render(request, 'assessment/assess.html', {})