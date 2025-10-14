from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import StudentRegistrationForm
# from .forms import EmployerRegistrationForm  # Uncomment when ready

def register(request):
    """
    Handles registration for both Students and Employers.
    For now, only Student registration is active.
    """

    if request.user.is_authenticated:
        return redirect('home')

    # Determine account type from POST (default to 'student')
    account_type = request.POST.get('account_type', 'student')

    # Select form based on account type
    if account_type == 'student':
        form_class = StudentRegistrationForm
    else:
        # form_class = EmployerRegistrationForm  # Placeholder for later
        form_class = StudentRegistrationForm  # Temporary fallback

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(
                    request,
                    f'Registration successful! Welcome to JobConnect as a {account_type.capitalize()}.'
                )
                return redirect('home')

            except IntegrityError as e:
                messages.error(request, "A database error occurred during registration. Please try again.")
                print(f"[IntegrityError] {e}")

            except Exception as e:
                messages.error(request, "An unexpected error occurred. Please contact support.")
                print(f"[Unexpected Error] {e}")

        else:
            messages.error(request, "Please correct the errors in the form.")

    else:
        form = form_class()

    return render(request, 'accounts/register.html', {'form': form})
