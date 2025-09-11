import re
from django import forms
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Transaction, Category


class PasswordStrengthMixin:
    """Mixin to add password strength validation"""
    
    def validate_password_strength(self, password):
        """
        Validate password strength according to FinTech standards:
        - At least 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one number
        - At least one symbol
        """
        errors = []
        
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long.")
        
        if not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter.")
        
        if not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter.")
        
        if not re.search(r'\d', password):
            errors.append("Password must contain at least one number.")
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>_]', password):
            errors.append("Password must contain at least one symbol (!@#$%^&*()_,.?\":{}|<>).")
        
        # Check for common weak patterns
        if password.lower() in ['password', '12345678', 'qwertyui']:
            errors.append("Password is too common. Please choose a more unique password.")
        
        return errors

class EnhancedUserCreationForm(UserCreationForm, PasswordStrengthMixin):
    """Enhanced signup form with password strength validation"""
    
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Username',
            'id': 'id_username'
        }),
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
    )
    
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'input-field',
            'placeholder': 'Password',
            'id': 'id_password1'
        }),
        help_text="Create a strong password with the requirements below."
    )
    
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'input-field',
            'placeholder': 'Confirm Password',
            'id': 'id_password2'
        }),
        help_text="Enter the same password as before, for verification."
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("A user with this username already exists.")
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1:
            errors = self.validate_password_strength(password1)
            if errors:
                raise ValidationError(errors)
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise ValidationError("The two password fields didn't match.")
        
        return password2


class TransactionForm(forms.ModelForm):
    """Form for adding a new transaction with category and payment details."""

    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),  # set dynamically in __init__
        required=False,
        widget=forms.Select(attrs={'class': 'input-field'})
    )

    class Meta:
        model = Transaction
        fields = [
            'date',
            'description',
            'amount',
            'transaction_type',
            'category',
            'merchant',
            'payment_method',
            'notes'
        ]

        widgets = {
            'date': forms.DateInput(
                attrs={'type': 'date', 'class': 'input-field'}
            ),
            'description': forms.TextInput(
                attrs={'class': 'input-field', 'placeholder': 'e.g., Groceries at S&R'}
            ),
            'amount': forms.NumberInput(
                attrs={'class': 'input-field', 'step': '0.01', 'placeholder': '0.00'}
            ),
            'transaction_type': forms.Select(
                attrs={'class': 'input-field'}
            ),
            'merchant': forms.TextInput(
                attrs={'class': 'input-field', 'placeholder': 'e.g., 7-Eleven'}
            ),
            'payment_method': forms.Select(
                attrs={'class': 'input-field'}
            ),
            'notes': forms.Textarea(
                attrs={'class': 'input-field', 'placeholder': 'Optional notes...', 'rows': 2}
            ),
        }

        labels = {
            'transaction_type': 'Type',
            'merchant': 'Merchant / Vendor',
            'payment_method': 'Payment Method',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # pass user in views
        super().__init__(*args, **kwargs)

        # Only leaf categories (those with a parent)
        qs = Category.objects.filter(parent__isnull=False)
        if user:
            qs = qs.filter(Q(user=user) | Q(user__isnull=True))
        self.fields['category'].queryset = qs.order_by('kind', 'parent__name', 'name')

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return amount

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        if category:
            # Force transaction_type to match category.kind
            cleaned_data['transaction_type'] = category.kind
        return cleaned_data

class CSVUploadForm(forms.Form):
    file = forms.FileField(
        label="Upload CSV File",
        help_text="CSV file containing transactions",
        widget=forms.ClearableFileInput(attrs={'class': 'input-field'})
    )