from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    user = request.user
    if user.user_type == 'applicant':
        return render(request, 'dashboard/applicant_dashboard.html')
    elif user.user_type == 'employer':
        return render(request, 'dashboard/employer_dashboard.html')
    elif user.user_type == 'admin':
        return render(request, 'dashboard/admin_dashboard.html')
    else:
        # Fallback for any other user type or if user_type is not set
        return render(request, 'home.html')
