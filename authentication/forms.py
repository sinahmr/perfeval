from django import forms
from . import models


class AddEmployeeForm(forms.ModelForm):
    user_type = forms.ChoiceField(label='نوع کاربر', choices=[('UA', 'مدیر واحد'), ('E', 'کارمند')])

    class Meta:
        model = models.Employee
        fields = ['username', 'password', 'first_name', 'last_name', 'father_name', 'personnel_code', 'national_code',
                  'year_of_birth', 'mobile', 'unit']
        widgets = {
            'password': forms.PasswordInput(),
        }
        help_texts = {
            'username': None
        }

    def save(self, commit=True):
        user_type = self.cleaned_data.get('user_type')
        del self.cleaned_data['user_type']

        if user_type == 'UA':
            models.UnitAdmin.create(**self.cleaned_data)
        else:
            models.Employee.create(**self.cleaned_data)


class LoginForm(forms.Form):
    username = forms.CharField(label='نام کاربری')
    password = forms.CharField(label='گذرواژه', widget=forms.PasswordInput())


class ChangeUsernameOrPasswordForm(forms.Form):
    username = forms.CharField(label='نام کاربری', max_length=50)
    password = forms.CharField(label='گذرواژه', max_length=50, widget=forms.PasswordInput())
    password_confirmation = forms.CharField(label='تکرار گذرواژه', max_length=50, widget=forms.PasswordInput())

    def clean(self):
        cd = self.cleaned_data
        password = cd.get('password')
        password_confirmation = cd.get('password_confirmation')
        if password != password_confirmation:
            raise forms.ValidationError('عدم تطابق گذرواژه و تکرار آن')
