# forms.py
from django import forms
from .models import Customer, Professional, Specialization, Answer, Question, JobDetail, AnswerJob


class CustomerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))

    class Meta:
        model = Customer
        fields = ['full_name', 'username', 'password', 'confirm_password']

        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Enter full name'}),
            'username': forms.TextInput(attrs={'placeholder': 'Enter user name'}),
        }

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
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))
    specialization = forms.ChoiceField(choices=[(tag.name, tag.value) for tag in Specialization])

    class Meta:
        model = Professional
        fields = ['full_name', 'username', 'specialization', 'number_of_jobs', 'years_of_experience', 'password',
                  'confirm_password']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Enter full name'}),
            'username': forms.TextInput(attrs={'placeholder': 'Enter user name'}),
            'specialization': forms.Select(attrs={'class': 'form-control'}),
            'number_of_jobs': forms.NumberInput(attrs={'placeholder': 'Enter number of jobs'}),
            'years_of_experience': forms.NumberInput(attrs={'placeholder': 'Enter years of experience'}),
        }
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the empty option from the choices
        self.fields['answer_value'].choices = [(i, i) for i in range(1, 6)]


class JobDetailForm(forms.ModelForm):
    class Meta:
        model = JobDetail
        fields = ['job_name', 'budget', 'detail_of_project', 'start_time', 'end_time']
        widgets = {
            'job_name': forms.TextInput(attrs={'placeholder': 'Enter job name'}),
            'budget': forms.NumberInput(attrs={'placeholder': 'Enter budget'}),
            'detail_of_project': forms.Textarea(attrs={'placeholder': 'Describe the project details'}),
            'start_time': forms.DateInput(attrs={'placeholder': 'Start time'}),
            'end_time': forms.DateInput(attrs={'placeholder': 'End time'}),
        }


class AnswerJobForm(forms.ModelForm):
    class Meta:
        model = AnswerJob
        fields = ['answer_value']
        widgets = {
            'answer_value': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)])
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the empty option from the choices
        self.fields['answer_value'].choices = [(i, i) for i in range(1, 6)]
