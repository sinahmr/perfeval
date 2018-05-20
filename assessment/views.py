from django.shortcuts import render
from . import forms


def add_criterion(request):
    if request.method == 'POST':
        form = forms.AddCriterionForm(request.POST)
    else:
        form = forms.AddCriterionForm()

    return render(request, 'assessment/add-criterion.html', {'form': form})


def criterion_list(request):
    return render(request, 'assessment/criterion-list.html', {})


def employee_list(request):
    return render(request, 'assessment/employee-list.html', {})


def show_employee(request, employee_id):
    return render(request, 'assessment/show-employee.html', {
        'has_assessment': True if employee_id % 2 == 0 else False
    })


def assessment_list(request):
    return render(request, 'assessment/assessment-list.html', {})


def assess(request, employee_id):
    return render(request, 'assessment/assess.html', {})