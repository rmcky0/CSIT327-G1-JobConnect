from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    # Applicant URLs
    path('applicant/applied-jobs/', views.applicant_applied_jobs, name='applicant_applied_jobs'),
    path('applicant/favorite-jobs/', views.applicant_favorite_jobs, name='applicant_favorite_jobs'),
    path('applicant/job-alerts/', views.applicant_job_alerts, name='applicant_job_alerts'),
    path('applicant/settings/', views.applicant_settings, name='applicant_settings'),
    # Employer URLs
    path('employer/profile/', views.employer_profile, name='employer_profile'),
    path('employer/post-job/', views.employer_post_job, name='employer_post_job'),
    path('employer/my-jobs/', views.employer_my_jobs, name='employer_my_jobs'),
    path('employer/settings/', views.employer_settings, name='employer_settings'),
    path('employer/job-applications/', views.employer_job_applications, name='employer_job_applications'),
    path('employer/candidate-detail/', views.employer_candidate_detail, name='employer_candidate_detail'),
]

