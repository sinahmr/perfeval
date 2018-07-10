from django import forms

from . import models


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
        model = models.Scale
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
                quan = models.QuantitativeCriterion.objects.create(formula=self.cleaned_data['quan_criterion_formula'],
                                                                   interpretation=self.cleaned_data[
                                                                       'quan_interpretation'])
                scale.set_quan_criterion(quan)
            if self.cleaned_data.get('qual_criterion_choices'):
                qual = models.QualitativeCriterion.objects.create(choices=self.cleaned_data['qual_criterion_choices'],
                                                                  interpretation=self.cleaned_data[
                                                                      'qual_interpretation'])
                scale.set_qual_criterion(qual)

            scale.save()
        return scale


class ScaleAnswerForm(forms.ModelForm):
    class Meta:
        model = models.ScaleAnswer
        fields = ['qualitativeAnswer', 'quantitativeAnswer']

    def __init__(self, *args, **kwargs):
        super(ScaleAnswerForm, self).__init__(*args, **kwargs)
        choices = self.instance.scale.qualitativeCriterion.get_choices_list()
        choices = [(c, c) for c in choices]
        self.fields['qualitativeAnswer'] = forms.ChoiceField(label='پاسخ کیفی', choices=choices)

    def clean(self):
        quan = self.cleaned_data.get('qualitativeAnswer', '')
        qual = self.cleaned_data.get('quantitativeAnswer', '')
        if not quan and not qual:
            raise forms.ValidationError('پاسخ را وارد کنید')

    def save(self, commit=True):
        ans = super(ScaleAnswerForm, self).save(commit=False)
        ans.carried_on = True
        if commit:
            ans.save()
        return ans
