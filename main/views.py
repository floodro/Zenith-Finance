import csv, datetime, logging, json, calendar

from django.utils.dateparse import parse_date
from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Sum

from .models import Profile
from .models import Transaction
from .models import Category

from .forms import TransactionForm
from .forms import CSVUploadForm    

logger = logging.getLogger(__name__)

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

# --- Dashboard View ---
@login_required
def dashboard_view(request):
    all_transactions = Transaction.objects.filter(user=request.user)
    recent_transactions = all_transactions[:5]
    
    total_income = all_transactions.filter(transaction_type='INCOME').aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    total_expenses = all_transactions.filter(transaction_type='EXPENSE').aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    total_balance = total_income - total_expenses

    context = {
        'total_balance': total_balance,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'transactions': recent_transactions,
    }
    return render(request, 'main/dashboard.html', context)

# --- Profile View ---
@login_required
def profile_view(request):
    # This view assumes a Profile model is linked via a OneToOneField
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        user.save()
        
        profile.contact_number = request.POST.get("contact_number")
        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("profile")
    
    return render(request, 'main/profile.html')

# --- Transactions Views ---
@login_required
def transactions_list_view(request):
    """Show user's transactions + transaction form."""
    user_transactions = Transaction.objects.filter(user=request.user)
    form = TransactionForm(user=request.user)  # pass user for category filtering
    context = {
        "transactions": user_transactions,
        "form": form,
    }
    return render(request, "main/transactions.html", context)

@login_required
def add_transaction_view(request):
    if request.method == "POST":
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, "✅ Transaction added successfully!")
        else:
            logger.warning(f"Transaction add failed: {form.errors}")
            messages.error(request, "❌ Failed to add transaction. Please check your inputs.")

    return redirect("transactions")

@login_required
def upload_transactions_view(request):
    """Handle CSV uploads for bulk transactions."""
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]
        decoded_file = file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_file)

        added, skipped = 0, 0

        for i, row in enumerate(reader, start=2):
            try:
                # Parse date
                try:
                    date = datetime.datetime.strptime(row["date"], "%Y-%m-%d").date()
                except ValueError:
                    logger.warning(f"Row {i} skipped: invalid date {row['date']}")
                    skipped += 1
                    continue

                # Parse amount
                try:
                    amount = Decimal(row["amount"])
                    if amount <= 0:
                        raise InvalidOperation
                except Exception:
                    logger.warning(f"Row {i} skipped: invalid amount {row['amount']}")
                    skipped += 1
                    continue

                # Transaction type
                valid_types = dict(Transaction.TRANSACTION_TYPE_CHOICES).keys()
                transaction_type = row["transaction_type"].upper()
                if transaction_type not in valid_types:
                    logger.warning(f"Row {i} skipped: invalid type {transaction_type}")
                    skipped += 1
                    continue

                # Category (optional)
                category = None
                if row.get("category"):
                    category = Category.objects.filter(name=row["category"]).first()

                # Duplicate check
                duplicate = Transaction.objects.filter(
                    user=request.user,
                    date=date,
                    description=row["description"],
                    amount=amount,
                    transaction_type=transaction_type,
                ).exists()
                if duplicate:
                    logger.info(f"Row {i} skipped: duplicate transaction")
                    skipped += 1
                    continue

                # Save transaction
                Transaction.objects.create(
                    user=request.user,
                    date=date,
                    description=row["description"],
                    amount=amount,
                    transaction_type=transaction_type,
                    category=category,
                    merchant=row.get("merchant", ""),
                    payment_method=row.get("payment_method", ""),
                    notes=row.get("notes", ""),
                )
                added += 1

            except Exception as e:
                logger.error(f"Row {i} skipped: unexpected error ({e})")
                skipped += 1

        # Final message (frontend-friendly)
        if added > 0:
            messages.success(request, f"✅ Imported {added} transactions. Skipped {skipped}.")
        else:
            messages.error(request, "❌ Upload failed.")

    else:
        messages.error(request, "❌ No file uploaded.")

    return redirect("transactions")

# --- Reports Views ---
@login_required
def reports_view(request):
    user = request.user

    # Group income & expenses by month
    monthly_data = (
        Transaction.objects.filter(user=user)
        .values("transaction_type", "date__month")
        .annotate(total=Sum("amount"))
    )

    months = [calendar.month_name[m] for m in range(1, 13)]
    income_data = [0] * 12
    expense_data = [0] * 12

    for entry in monthly_data:
        month_idx = entry["date__month"] - 1
        if entry["transaction_type"] == "INCOME":
            income_data[month_idx] = float(entry["total"])
        elif entry["transaction_type"] == "EXPENSE":
            expense_data[month_idx] = float(entry["total"])

    # Group expenses by category
    expense_categories = (
        Transaction.objects.filter(user=user, transaction_type="EXPENSE", category__isnull=False)
        .values("category__name")
        .annotate(total=Sum("amount"))
    )

    category_labels = [c["category__name"] for c in expense_categories]
    category_totals = [float(c["total"]) for c in expense_categories]

    context = {
        "months": json.dumps(months),
        "income_data": json.dumps(income_data),
        "expense_data": json.dumps(expense_data),
        "category_labels": json.dumps(category_labels),
        "category_totals": json.dumps(category_totals),
    }
    
    return render(request, 'main/reports.html', context)

# --- Settings View ---
@login_required
def settings_view(request):
    return render(request, 'main/settings.html')