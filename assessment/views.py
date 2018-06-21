from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import ListView

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
        if self.get_queryset() is None or len(self.get_queryset()) < 1:
            not_found=True
        else:
            not_found=False
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

#
def show_employee(request, employee_id):
    return render(request, 'assessment/show-employee.html', {
        'has_assessment': True if employee_id % 2 == 0 else False
    })
#
#
# def assessment_list(request):
#     return render(request, 'assessment/assessment-list.html', {})
#
#
# def assess(request, employee_id):
#     return render(request, 'assessment/assess.html', {})