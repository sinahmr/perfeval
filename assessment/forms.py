from django import forms

from assessment.models import Assessment, Scale, ScaleAnswer, Season, PunishmentReward
from authentication.models import Employee


class AddScaleForm(forms.ModelForm):
    qualitativeCriterion = None
    qual_criterion_choices = forms.CharField(label='گزینه‌های کیفی', required=False,
                                             widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}),
                                             help_text='هر گزینه را در یک سطر جدا بنویسید')
    qual_interpretation = forms.CharField(label='نحوه‌ی تفسیر کیفی',
                                          widget=forms.Textarea(attrs={'rows': 2, 'cols': 50}), required=False)

    quantitativeCriterion = None
    quan_criterion_formula = forms.CharField(label='فرمول محاسبه‌ی کمی', max_length=200, required=False)
    quan_interpretation = forms.CharField(label='نحوه‌ی تفسیر کمی',
                                          widget=forms.Textarea(attrs={'rows': 2, 'cols': 50}), required=False)

    class Meta:
        model = Scale
        fields = ['title', 'description', 'qual_criterion_choices', 'qual_interpretation', 'quan_criterion_formula',
                  'quan_interpretation']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AddScaleForm, self).__init__(*args, **kwargs)

    def clean(self):
        quan = self.cleaned_data.get('quan_criterion_formula', '')
        qual = self.cleaned_data.get('qual_criterion_choices', '')
        if not quan and not qual:
            raise forms.ValidationError('باید حداقل یکی از موارد «فرمول محاسبه‌ی کمی» یا «گزینه‌های کیفی» را پر کنید')

        quan_i = self.cleaned_data.get('quan_interpretation', '')
        qual_i = self.cleaned_data.get('qual_interpretation', '')
        if (quan and not quan_i) or (qual and not qual_i):
            raise forms.ValidationError('نحوه‌ی تفسیر را وارد کنید')

    def save(self, commit=True):
        scale = super(AddScaleForm, self).save(commit=False)
        quan = None
        qual = None
        quan_interpretation = None
        qual_interpretation = None
        if commit:
            if self.cleaned_data.get('quan_criterion_formula'):
                quan = self.cleaned_data.get('quan_criterion_formula')
                quan_interpretation = self.cleaned_data['quan_interpretation']
            if self.cleaned_data.get('qual_criterion_choices'):
                qual = self.cleaned_data['qual_criterion_choices']
                qual_interpretation = self.cleaned_data['qual_interpretation']
            admin = self.user.get_job()
            scale = admin.add_scale(scale, quan, qual, quan_interpretation, qual_interpretation)
            scale.save()
        return scale


class ScaleAnswerForm(forms.ModelForm):
    class Meta:
        model = ScaleAnswer
        fields = ['qualitativeAnswer', 'quantitativeAnswer']

    def __init__(self, *args, **kwargs):
        super(ScaleAnswerForm, self).__init__(*args, **kwargs)
        if self.instance.get_scale_qualitative_criterion():
            self.choices = self.instance.get_scale_qualitative_criterion().get_choices_list()
            choices = [(i, c) for i, c in enumerate(self.choices)]
            self.fields['qualitativeAnswer'] = forms.ChoiceField(label='پاسخ کیفی', choices=choices)
        else:
            del self.fields['qualitativeAnswer']

        if self.instance.get_scale_quantitative_criterion():
            pass
        else:
            del self.fields['quantitativeAnswer']

    def clean(self):
        quan = self.cleaned_data.get('quantitativeAnswer', '')
        qual = self.cleaned_data.get('qualitativeAnswer', '')
        if self.instance.get_scale_qualitative_criterion() and not qual:
            raise forms.ValidationError('پاسخ کیفی را وارد کنید')
        if self.instance.get_scale_quantitative_criterion() and not quan:
            raise forms.ValidationError('پاسخ کمی را وارد کنید')

    def save(self, commit=True):
        ans = super(ScaleAnswerForm, self).save(commit=False)
        if ans.get_qualitative_answer():
            index_of_choice = int(ans.get_qualitative_answer())
            ans.set_qualitative_answer(self.choices[index_of_choice])
        ans.set_carried_on(True)
        if commit:
            ans.save()
        return ans


class CreateAssessmentForm(forms.ModelForm):
    assessor = forms.ModelChoiceField(label='ارزیاب', queryset=Employee.objects.all())  # TODO error
    scales = forms.ModelMultipleChoiceField(label='معیار ها', queryset=Scale.objects.all())

    class Meta:
        model = Assessment
        fields = ['assessor', 'scales']

    def __init__(self, *args, **kwargs):
        self.assessed = kwargs.pop('assessed')
        super(CreateAssessmentForm, self).__init__(*args, **kwargs)
        assessors_queryset = Employee.objects.exclude(id=self.assessed.get_id())
        self.fields['assessor'] = forms.ModelChoiceField(label='ارزیاب', queryset=assessors_queryset)  # TODO error

    def save(self, commit=True):
        assessed = self.assessed
        assessor = self.cleaned_data['assessor']

        if commit:
            return assessor.create_assessment(assessor, assessed, self.cleaned_data['scales'])


class PunishmentRewardForm(forms.ModelForm):
    class Meta:
        model = PunishmentReward
        fields = ['type', 'method']


class AddSeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = ['title', 'active']

    def save(self, commit=True):
        season = super(AddSeasonForm, self).save(commit=False)
        if self.cleaned_data['active']:
            Season.objects.activate_season(season)
        if commit:
            season.save()
        return season


class ChangeSeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = ['active']

    def save(self, commit=True):
        season = super(ChangeSeasonForm, self).save(commit=False)
        if self.cleaned_data['active']:
            Season.objects.activate_season(season)
        if commit:
            season.save()
        return season
