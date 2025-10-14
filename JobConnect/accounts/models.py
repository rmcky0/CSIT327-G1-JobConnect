from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Make email required and unique for authentication
    email = models.EmailField(unique=True, blank=False)
    
    # Define which fields Django should use for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username'] # 'username' remains required for createsuperuser by default
    EMAIL_FIELD = 'email'

    USER_TYPE_CHOICES = (
        ('applicant', 'Applicant'),
        ('employer', 'Employer'),
        # Note: The 'admin' user_type is mostly informational. Django uses is_staff/is_superuser for actual admin permissions.
        ('admin', 'Admin') 
    )
    
    user_type = models.CharField(
        max_length=10, 
        choices=USER_TYPE_CHOICES, 
        default='applicant',
        verbose_name='User Type'
    )
    
    def __str__(self):
        return self.email

class ApplicantProfile(models.Model):
    """Placeholder for applicant-specific data."""
    # Added related_name to prevent reverse relationship clashes
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        primary_key=True,
        related_name='applicant_profile'
    )
    
    def __str__(self):
        return f"Applicant Profile for {self.user.email}"

class EmployerProfile(models.Model):
    """Placeholder for employer-specific data."""
    # Added related_name to prevent reverse relationship clashes
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        primary_key=True,
        related_name='employer_profile'
    )
    
    # Example field to show employer-specific data
    company_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Employer Profile for {self.user.email}"