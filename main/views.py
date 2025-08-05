from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Sum
from decimal import Decimal
from .models import Transaction
from .forms import TransactionForm

def signup(request):
    """Handle user signup."""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("signup")

        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, "Account created successfully! Please log in.")
        return redirect("login")

    return render(request, 'main/signup.html')

def login(request):
    """Handle user login."""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login successful!")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password!")
            return redirect("login")

    return render(request, 'main/login.html')

def logout(request):
    """Log out the user."""
    auth_logout(request)
    messages.success(request, "You have been logged out!")
    return redirect("login")

@login_required # Use this decorator instead of the manual check
def dashboard(request):
    """Render the user dashboard with dynamic data."""
    
    # Get all transactions for the currently logged-in user
    transactions = Transaction.objects.filter(user=request.user)
    
    # Calculate total income
    total_income = transactions.filter(transaction_type='INCOME').aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    
    # Calculate total expenses
    total_expenses = transactions.filter(transaction_type='EXPENSE').aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    
    # Calculate total balance
    total_balance = total_income - total_expenses

    context = {
        'user': request.user,
        'transactions': transactions,
        'total_balance': total_balance,
        'total_income': total_income,
        'total_expenses': total_expenses,
    }

    return render(request, 'main/dashboard.html', context)

def is_admin(user):
    return user.is_staff or user.is_superuser

# In views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

# ... your other views

@login_required
def profile(request):
    """
    Handle user profile display and updates.
    """
    if request.method == "POST":
        # Get the form data from the POST request
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        
        # Update the user object
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        messages.success(request, "Your profile has been updated successfully!")
        return redirect("profile")

    # For a GET request, just render the page with the user's current data
    return render(request, 'main/profile.html')

def transactions(request):
    """Render the transactions page."""
    if request.method == "POST":
        # Handle transaction creation logic here
        messages.success(request, "Transaction added successfully!")
        return redirect("transactions")

    user_transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'main/transactions.html', {'transactions': user_transactions})

def reports(request):
    """Render the reports page."""
    # Here you can implement logic to generate reports based on transactions
    return render(request, 'main/reports.html')

def settings(request):
    """Render the settings page."""
    if request.method == "POST":
        # Handle settings update logic here
        messages.success(request, "Settings updated successfully!")
        return redirect("settings")

    return render(request, 'main/settings.html')

@login_required
def transaction_list(request):
    """
    Display a full list of all transactions for the logged-in user.
    """
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'main/transactions.html', {'transactions': transactions})

@login_required
def add_transaction(request):
    """
    Handle the creation of a new transaction.
    """
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            # Create a Transaction instance but don't save it to the database yet
            transaction = form.save(commit=False)
            # Assign the current logged-in user to the transaction
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction added successfully!')
            return redirect('transaction_list')
    else:
        # If it's a GET request, create an empty form instance
        form = TransactionForm()
    
    return render(request, 'main/add_transaction.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def admin_upload_transactions(request):
    """Handle the upload of transactions by admin."""
    if request.method == "POST":
        # Handle file upload and processing logic here
        messages.success(request, "Transactions uploaded successfully!")
        return redirect("transaction_list")

