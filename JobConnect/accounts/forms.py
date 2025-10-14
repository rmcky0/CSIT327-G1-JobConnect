from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, ApplicantProfile, EmployerProfile
from django.contrib.auth import get_user_model

User = get_user_model() 

# --- Base Registration Form for both Applicant and Employer ---
class ApplicantRegistrationForm(UserCreationForm):
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
        choices=[('applicant', 'Applicant'), ('employer', 'Employer')],
        widget=forms.Select(attrs={'class': 'form-select'}),
        # Set the default choice for the Applicant form explicitly
        initial='applicant' 
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the default 'username' field which is often redundant when using email
        if 'username' in self.fields:
            del self.fields['username']

    def save(self, commit=True):
        """Create either a Applicant or Employer user with their profile."""
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        # Use the value from the cleaned data, defaulting to 'applicant' if not provided
        user.user_type = self.cleaned_data.get('account_type', 'applicant') 

        if commit:
            user.save()

            # Create profile depending on user type
            if user.user_type == 'applicant':
                ApplicantProfile.objects.create(user=user)
            elif user.user_type == 'employer':
                EmployerProfile.objects.create(user=user)

        return user

# --- NEW Employer Registration Form (Inherits from Applicant form) ---
class EmployerRegistrationForm(ApplicantRegistrationForm):
    """
    Inherits all fields and validation from ApplicantRegistrationForm, 
    but defaults the account_type field to 'employer'.
    """
    # Overrides the account_type field to change the initial/default value
    account_type = forms.ChoiceField(
        choices=[('applicant', 'Applicant'), ('employer', 'Employer')],
        widget=forms.Select(attrs={'class': 'form-select'}),
        initial='employer' # <<< This is the key difference
    )

    # Note: No need to redefine Meta or save(), as they are inherited and work correctly
    # based on the value passed for 'account_type'.

# --- User Login Form (Unchanged) ---
class UserLoginForm(AuthenticationForm):
    # Customize the username field to be labeled/placeholder as "Email address"
    username = forms.CharField(
        label="Email address",
        widget=forms.TextInput(attrs={
            'placeholder': 'Email address',
            'class': 'form-control',
            'id': 'id_username'
        })
    )
    # Customize the password field
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-control',
            'id': 'id_password'
        })
    )
    
    # You can optionally add a 'Remember Me' field if you want to control session expiration
    remember_me = forms.BooleanField(
        required=False,
        label='Remember Me',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        fields = ['username', 'password', 'remember_me']