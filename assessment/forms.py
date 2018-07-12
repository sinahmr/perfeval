from django import forms

from assessment.models import Assessment, Scale, ScaleAnswer, QuantitativeCriterion, QualitativeCriterion, Season, \
    PunishmentReward
from authentication.models import User


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
        if commit:
            if self.cleaned_data.get('quan_criterion_formula'):
                quan = QuantitativeCriterion.objects.create(formula=self.cleaned_data['quan_criterion_formula'],
                                                            interpretation=self.cleaned_data[
                                                                'quan_interpretation'])
                scale.set_quantitative_criterion(quan)
            if self.cleaned_data.get('qual_criterion_choices'):
                qual = QualitativeCriterion.objects.create(choices=self.cleaned_data['qual_criterion_choices'],
                                                           interpretation=self.cleaned_data[
                                                               'qual_interpretation'])
                scale.set_qualitative_criterion(qual)

            scale.save()
        return scale


class ScaleAnswerForm(forms.ModelForm):
    class Meta:
        model = ScaleAnswer
        fields = ['qualitativeAnswer', 'quantitativeAnswer']

    def __init__(self, *args, **kwargs):
        super(ScaleAnswerForm, self).__init__(*args, **kwargs)
        if self.instance.scale.get_qualitative_criterion():
            self.choices = self.instance.scale.get_qualitative_criterion().get_choices_list()
            choices = [(i, c) for i, c in enumerate(self.choices)]
            self.fields['qualitativeAnswer'] = forms.ChoiceField(label='پاسخ کیفی', choices=choices)
        else:
            del self.fields['qualitativeAnswer']

        if self.instance.scale.get_quantitative_criterion():
            pass
        else:
            del self.fields['quantitativeAnswer']

    def clean(self):
        quan = self.cleaned_data.get('quantitativeAnswer', '')
        qual = self.cleaned_data.get('qualitativeAnswer', '')
        if self.instance.scale.get_qualitative_criterion() and not qual:
            raise forms.ValidationError('پاسخ کیفی را وارد کنید')
        if self.instance.scale.get_quantitative_criterion() and not quan:
            raise forms.ValidationError('پاسخ کمی را وارد کنید')

    def save(self, commit=True):
        ans = super(ScaleAnswerForm, self).save(commit=False)
        index_of_choice = int(ans.get_qualitative_answer())
        ans.set_qualitative_answer(self.choices[index_of_choice])
        ans.carried_on = True
        if commit:
            ans.save()
        return ans


class CreateAssessmentForm(forms.ModelForm):
    a_assessor = forms.ModelChoiceField(label='ارزیاب', queryset=User.objects.all().employees())  # TODO error
    scales = forms.ModelMultipleChoiceField(label='معیار ها', queryset=Scale.objects.all())

    class Meta:
        model = Assessment
        fields = ['a_assessor', 'scales', ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(CreateAssessmentForm, self).__init__(*args, **kwargs)
        assessors_queryset = User.objects.exclude(id=self.user.id).employees()
        self.fields['a_assessor'] = forms.ModelChoiceField(label='ارزیاب', queryset=assessors_queryset)  # TODO error

    def save(self, commit=True):
        assessed = self.user.get_employee()
        assessor = self.cleaned_data['a_assessor'].get_employee()
        assessment = Assessment.objects.create(assessor=assessor,
                                               assessed=assessed)
        if commit:
            assessment.save()
            for sc in self.cleaned_data['scales']:
                ScaleAnswer.objects.create(scale=sc, assessment=assessment)
            PunishmentReward.objects.create(assessment=assessment)
        return assessment


class PunishmentRewardForm(forms.ModelForm):
    class Meta:
        model = PunishmentReward
        fields = ['type', 'method']


class AddSeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = ['title']
