from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    user = request.user
    if user.user_type == 'applicant':
        # The main dashboard view now renders the overview template.
        return render(request, 'dashboard/applicant_overview.html')
    elif user.user_type == 'employer':
        return render(request, 'dashboard/employer_dashboard.html')
    elif user.user_type == 'admin':
        return render(request, 'dashboard/admin_dashboard.html')
    else:
        # Fallback for any other user type or if user_type is not set
        return render(request, 'home.html')

@login_required
def applicant_applied_jobs(request):
    context = {} # Add any context needed for the template
    return render(request, 'dashboard/applicant_applied_jobs.html', context)

@login_required
def applicant_favorite_jobs(request):
    context = {} # Add any context needed for the template
    return render(request, 'dashboard/applicant_favorite_jobs.html', context)

@login_required
def applicant_job_alerts(request):
    context = {} # Add any context needed for the template
    return render(request, 'dashboard/applicant_job_alerts.html', context)

@login_required
def applicant_settings(request):
    return render(request, 'dashboard/applicant_settings.html')
