# forms.py
from django import forms
from .models import Customer, Professional, Specialization, Answer, Question, JobDetail, AnswerJob


class CustomerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ['full_name', 'username', 'password', 'confirm_password']

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if Customer.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        return cleaned_data


class ProfessionalRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    specialization = forms.ChoiceField(choices=[(tag.name, tag.value) for tag in Specialization])

    class Meta:
        model = Professional
        fields = ['full_name', 'username', 'specialization', 'number_of_jobs', 'years_of_experience', 'password',
                  'confirm_password']

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if Professional.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        return cleaned_data


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_value']
        widgets = {
            'answer_value': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)])
        }


class JobDetailForm(forms.ModelForm):
    class Meta:
        model = JobDetail
        fields = ['job_name', 'budget']


class AnswerJobForm(forms.ModelForm):
    class Meta:
        model = AnswerJob
        fields = ['answer_value']
        widgets = {
            'answer_value': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)])
        }
