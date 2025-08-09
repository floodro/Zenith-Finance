from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Sum

from .models import Transaction
from .forms import TransactionForm

# --- Authentication Views ---

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
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
        messages.success(request, "Account created! Please log in.")
        return redirect("login")
        
    return render(request, 'main/signup.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("login")
    return render(request, 'main/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")

# --- Core App Views ---

@login_required
def dashboard_view(request):
    all_transactions = Transaction.objects.filter(user=request.user)
    recent_transactions = all_transactions[:5]
    
    total_income = all_transactions.filter(transaction_type='INCOME').aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    total_expenses = all_transactions.filter(transaction_type='EXPENSE').aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    total_transfers = all_transactions.filter(transaction_type='TRANSFER').aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    total_refunds = all_transactions.filter(transaction_type='REFUND').aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    total_balance = total_income - total_expenses

    context = {
        'total_balance': total_balance,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'total_transfers': total_transfers,
        'total_refunds': total_refunds,
        'transactions': recent_transactions,
    }
    return render(request, 'main/dashboard.html', context)

@login_required
def profile_view(request):
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        user.profile.contact_number = request.POST.get("contact_number")
        user.save()
        user.profile.save() # This is now safe because the profile is guaranteed to exist
        messages.success(request, "Profile updated successfully!")
        return redirect("profile")
    
    return render(request, 'main/profile.html')

@login_required
def transactions_list_view(request):
    user_transactions = Transaction.objects.filter(user=request.user)
    context = {'transactions': user_transactions}
    return render(request, 'main/transactions.html', context)

@login_required
def add_transaction_view(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction added successfully!')
            return redirect('transactions')
    else:
        form = TransactionForm()
    
    return render(request, 'main/add_transaction.html', {'form': form})

@login_required
def reports_view(request):
    return render(request, 'main/reports.html')

@login_required
def settings_view(request):
    return render(request, 'main/settings.html')
