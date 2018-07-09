from django import forms

from . import models


class AddScaleForm(forms.Form):
    title = forms.CharField(label='عنوان', max_length=50)
    description = forms.CharField(label='توضیحات', widget=forms.Textarea(attrs={'rows': 2, 'cols': 50}), required=False)
    quantitative_criterion_formula = forms.CharField(label='فرمول محاسبه‌ی کمی', max_length=200, required=False)
    qualitative_criterion_choices = forms.CharField(label='گزینه‌های کیفی', required=False,
                                                    widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}),
                                                    help_text='هر گزینه را در یک سطر جدا بنویسید')
    interpretation_rule = forms.CharField(label='نحوه‌ی تفسیر', widget=forms.Textarea(attrs={'rows': 2, 'cols': 50}))

    def clean(self):
        quan = self.cleaned_data.get('quantitative_criterion_choices', '')
        qual = self.cleaned_data.get('qualitative_criterion_choices', '')
        if not quan and not qual:
            raise forms.ValidationError('باید حداقل یکی از موارد «فرمول محاسبه‌ی کمی» یا «گزینه‌های کیفی» را پر کنید')


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
