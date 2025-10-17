from django.urls import path
from . import views

app_name = 'employer_profile'

urlpatterns = [
    path('profile/company-info/', views.employer_profile_setup_step1, name='employer_profile_setup_step1'),
    path('profile/founding-info/', views.employer_profile_setup_step2, name='employer_profile_setup_step2'),
    path('profile/contact/', views.employer_profile_setup_step3, name='employer_profile_setup_step3'),
    path('profile/complete/', views.employer_profile_completion, name='employer_profile_completion'),
]