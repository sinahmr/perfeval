from django.shortcuts import render
from . import forms


def request_new_assessment(request):
    if request.method == 'POST':
        form = forms.RequestNewAssessmentForm(request.POST)
    else:
        form = forms.RequestNewAssessmentForm()

    return render(request, 'validation/request-new-assessment.html', {'form': form})


def objections_list(request):
    return render(request, 'validation/objections-list.html', {})


def show_assessment_and_objection(request, objection_id):
    return render(request, 'validation/show-assessment-and-objection.html', {})


def inconsistency_list(request):
    return render(request, 'validation/inconsistency-list.html', {})


def resolve_inconsistency(request, inconsistency_id):
    return render(request, 'validation/resolve-inconsistency.html', {})