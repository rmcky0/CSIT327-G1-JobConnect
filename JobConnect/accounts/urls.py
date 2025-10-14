from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/applicant/', views.applicant_dashboard, name='applicant_dashboard'),
    path('dashboard/employer/', views.employer_dashboard, name='employer_dashboard'),
    # path('logout/', views.LogoutView.as_view(), name='logout'),
    # path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    # path('profile/', views.ProfileView.as_view(), name='profile'),
    # path('profile/edit/', views.EditProfileView.as_view(), name='edit_profile'),
]