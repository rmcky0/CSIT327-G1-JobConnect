from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
# Assuming you have created EmployerRegistrationForm
from .forms import ApplicantRegistrationForm, UserLoginForm, EmployerRegistrationForm 

# --- Helper function to determine success URL ---
def get_user_dashboard_url(user):
    """Returns the correct dashboard URL based on the user's type."""
    # Assuming your User model has a 'user_type' field ('applicant' or 'employer')
    if user.user_type == 'employer':
        return 'accounts:employer_dashboard'
    else: # Default or applicant
        return 'accounts:applicant_dashboard'

# --- Register View (Updated for GET parameter pre-selection) ---
def register(request):
    """
    Handles registration for both Applicants and Employers.
    Initializes the form based on a GET parameter if available.
    """
    if request.user.is_authenticated:
        # Redirect authenticated users to their respective dashboards
        return redirect(get_user_dashboard_url(request.user)) 

    # 1. Determine the account type from GET (on initial load) or POST (on submission)
    account_type_param = request.POST.get('account_type') or request.GET.get('account_type')
    
    # 2. Set the current account type, defaulting to 'applicant'
    account_type = account_type_param if account_type_param in ['applicant', 'employer'] else 'applicant'

    # 3. Select the correct form class based on the type
    if account_type == 'employer':
        form_class = EmployerRegistrationForm  
    else:
        form_class = ApplicantRegistrationForm

    if request.method == 'POST':
        # On POST, form data includes account_type, so no 'initial' is needed
        form = form_class(request.POST) 
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(
                    request,
                    f'Registration successful! Welcome to JobConnect as a {user.user_type.capitalize()}.'
                )
                # Redirect to the specific dashboard after registration
                return redirect(get_user_dashboard_url(user))

            except IntegrityError as e:
                messages.error(request, "An account with this email already exists.")
            except Exception as e:
                messages.error(request, "An unexpected error occurred. Please contact support.")

        else:
            messages.error(request, "Please correct the errors in the form.")
    
    else:
        # On GET, initialize the form with the pre-selected type from the URL parameter
        form = form_class(initial={'account_type': account_type})

    return render(request, 'accounts/register.html', {'form': form})

# --- Login View (Updated for post-login dashboard redirection) ---
def user_login(request):
    """
    Handles user login and redirects to the appropriate dashboard.
    """
    if request.user.is_authenticated:
        # Redirect authenticated users to their respective dashboards
        return redirect(get_user_dashboard_url(request.user)) 

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')

            user = authenticate(username=username, password=password)
            
            if user is not None:
                # Handle 'Remember Me' logic
                if not remember_me:
                    request.session.set_expiry(0) 
                else:
                    request.session.set_expiry(60 * 60 * 24 * 14) 
                    
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name}!")
                
                # --- NEW REDIRECTION LOGIC ---
                # Check for 'next' parameter first (for protected pages)
                next_url = request.POST.get('next')
                
                if next_url:
                    return redirect(next_url)
                else:
                    # Redirect to the user's specific dashboard
                    return redirect(get_user_dashboard_url(user))
            else:
                messages.error(request, "Invalid email or password.")
        else:
            # --- ADD THIS DEBUG LINE ---
            print("FORM ERRORS:", form.errors.as_json())
            # --- END DEBUG LINE ---
            messages.error(request, "Please correct the errors in the form.")
    
    else:
        form = UserLoginForm()
        
    next_url = request.GET.get('next')

    context = {
        'form': form,
        'next': next_url
    }
    return render(request, 'accounts/login.html', context)

# --- Logout View ---
def user_logout(request):
    """Logs the user out and redirects to home."""
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

# --- Applicant Dashboard (temporary) ---
def applicant_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    return render(request, 'accounts/applicant_dashboard.html')

# --- Employer Dashboard (temporary) ---
def employer_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    return render(request, 'accounts/employer_dashboard.html')