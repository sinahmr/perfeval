from django import forms


class RequestNewAssessmentForm(forms.Form):
    explanation = forms.CharField(label='دلیل', widget=forms.Textarea(attrs={'rows': 2, 'cols': 50}))
