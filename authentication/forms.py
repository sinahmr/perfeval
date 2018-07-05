from django import forms

from assessment.models import Assessment, Scale
from authentication.models import Employee
from . import models


class AddEmployeeForm(forms.ModelForm):
    password_confirmation = forms.CharField(label='تکرار گذرواژه', widget=forms.PasswordInput())
    employee_units = forms.ModelMultipleChoiceField(label='واحدها', queryset=models.Unit.objects.all())

    class Meta:
        model = models.User
        fields = ['username', 'password', 'password_confirmation', 'first_name', 'last_name', 'father_name',
                  'personnel_code', 'national_code', 'year_of_birth', 'mobile', 'employee_units']
        required_fields = ['username', 'password', 'password_confirmation', 'first_name', 'last_name', 'personnel_code',
                           'national_code', 'mobile', 'employee_units']
        widgets = {'password': forms.PasswordInput()}
        help_texts = {'username': None}

    def clean(self):
        cd = self.cleaned_data
        password = cd.get('password')
        password_confirmation = cd.get('password_confirmation')
        if password != password_confirmation:
            raise forms.ValidationError('عدم تطابق گذرواژه و تکرار آن')

    def save(self, commit=True):
        employee = models.Employee.objects.create()
        employee.set_units(list(self.cleaned_data['employee_units']))
        employee.save()

        user = super(AddEmployeeForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.set_job(employee)

        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label='نام کاربری')
    password = forms.CharField(label='گذرواژه', widget=forms.PasswordInput())


class ChangeUsernameOrPasswordForm(forms.ModelForm):
    password_confirmation = forms.CharField(label='تکرار گذرواژه', widget=forms.PasswordInput())

    class Meta:
        model = models.User
        fields = ['username', 'password', 'password_confirmation']
        required_fields = ['username', 'password', 'password_confirmation']
        widgets = {'password': forms.PasswordInput()}
        help_texts = {'username': None}

    def clean(self):
        cd = self.cleaned_data
        password = cd.get('password')
        password_confirmation = cd.get('password_confirmation')
        if password != password_confirmation:
            raise forms.ValidationError('عدم تطابق گذرواژه و تکرار آن')

    def save(self, commit=True):
        user = super(ChangeUsernameOrPasswordForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class CreateAssessmentForm(forms.ModelForm):
    assessor = forms.ModelChoiceField(label='ارزیاب', queryset=models.User.objects.all().employees())
    scales = forms.ModelMultipleChoiceField(label='معیار ها', queryset=Scale.objects.all())

    class Meta:
        model = Assessment
        fields = ['assessor', 'scales',]


    def save(self, commit=True,*args, **kwargs):
        asssessment = super(CreateAssessmentForm, self).save(commit=False, *args,**kwargs)
        request = None
        if 'request' in kwargs.keys():
            request = kwargs.pop('request')
        asssessment.set_season()
        asssessment.set_assessed(Employee.objects.get(id=request.user.id))
        if commit:
            asssessment.save()
        return asssessment