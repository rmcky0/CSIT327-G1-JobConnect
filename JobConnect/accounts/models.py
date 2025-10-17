from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']
    EMAIL_FIELD = 'email'

    USER_TYPE_CHOICES = (
        ('applicant', 'Applicant'),
        ('employer', 'Employer'),
        ('admin', 'Admin') 
    )
    
    user_type = models.CharField(
        max_length=10, 
        choices=USER_TYPE_CHOICES, 
        default='applicant',
        verbose_name='User Type'
    )
    
    @property
    def profile(self):
        """
        Returns the specific profile instance (Applicant or Employer) 
        based on the user_type. This simplifies template access.
        """
        if self.user_type == 'applicant':
            return self.applicant_profile_rel 
        elif self.user_type == 'employer':
            return self.employer_profile_rel
        return None 
    
    def __str__(self):
        return self.email


class ApplicantProfile(models.Model):
    """Stores data specific to applicants."""
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        primary_key=True,
        related_name='applicant_profile_rel' 
    )
    
    image = models.ImageField(
        upload_to='applicant_avatars/', 
        default='default-avatar.png', 
        null=True, 
        blank=True
    )
    
    def __str__(self):
        return f"Applicant Profile for {self.user.email}"

class EmployerProfile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        primary_key=True,
        related_name='employer_profile_rel' 
    )
    
    # --- Step 1: Company Info (Existing Fields) ---
    company_name = models.CharField(max_length=255, blank=True, null=True)
    about_us = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='employer_documents/logos/', blank=True, null=True)
    business_permit = models.FileField(upload_to='employer_documents/permits/', blank=True, null=True)

    # --- Step 2: Founding Info (NEW FIELDS) ---
    ORGANIZATION_CHOICES = [
        ('corp', 'Corporation'), ('llc', 'LLC'), ('solo', 'Sole Proprietorship')
    ]
    INDUSTRY_CHOICES = [
        ('tech', 'Technology'), 
        ('finance', 'Finance'), 
        ('health', 'Healthcare'),
        ('retail', 'Retail'),               # Added
        ('manu', 'Manufacturing'),          # Added
        ('edu', 'Education'),               # Added
        ('nonprofit', 'Non-Profit'),        # Added
        ('construction', 'Construction'),   # Added
        ('other', 'Other'),                 # Added
    ]
    TEAM_SIZE_CHOICES = [
        ('1-10', '1-10 Employees'), ('11-50', '11-50 Employees'), ('51+', '51+ Employees')
    ]
    
    organization_type = models.CharField(max_length=50, choices=ORGANIZATION_CHOICES, blank=True, null=True)
    industry_type = models.CharField(
        max_length=50, 
        choices=INDUSTRY_CHOICES, 
        blank=True, 
        null=True
    )
    team_size = models.CharField(max_length=20, choices=TEAM_SIZE_CHOICES, blank=True, null=True)
    year_established = models.DateField(blank=True, null=True)
    company_website = models.URLField(max_length=200, blank=True, null=True)
    company_vision = models.TextField(blank=True, null=True)

    # --- Step 3: Contact (NEW FIELDS) ---
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)

    setup_step = models.IntegerField(default=1) 
    
    def __str__(self):
        return f"Employer Profile for {self.user.email}"