from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, StudentProfile, EmployerProfile

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email address',
            'class': 'form-control'
        })
    )
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'First name',
            'class': 'form-control'
        })
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Last name',
            'class': 'form-control'
        })
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-control'
        })
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm password',
            'class': 'form-control'
        })
    )
    terms_and_conditions = forms.BooleanField(required=True)
    account_type = forms.ChoiceField(
        choices=[('student', 'Applicant'), ('employer', 'Employer')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'account_type',
        ]

    def save(self, commit=True):
        """Create either a Student or Employer user with their profile."""
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.user_type = self.cleaned_data.get('account_type', 'student')

        if commit:
            user.save()

            # Create profile depending on user type
            if user.user_type == 'student':
                StudentProfile.objects.create(user=user)
            elif user.user_type == 'employer':
                EmployerProfile.objects.create(user=user)

        return user
