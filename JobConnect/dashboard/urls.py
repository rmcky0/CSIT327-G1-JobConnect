from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('applied-jobs/', views.applicant_applied_jobs, name='applicant_applied_jobs'),
    path('favorite-jobs/', views.applicant_favorite_jobs, name='applicant_favorite_jobs'),
    path('job-alerts/', views.applicant_job_alerts, name='applicant_job_alerts'),
    path('applicant/settings/', views.applicant_settings, name='applicant_settings'),
]
