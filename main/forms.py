from django import forms
from django.db.models import Q
from .models import Transaction, Category


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