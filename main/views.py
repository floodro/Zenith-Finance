from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Sum
from decimal import Decimal
from .models import Transaction

def index(request):
    """Render the index page."""
    return render(request, 'main/index.html', {})

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