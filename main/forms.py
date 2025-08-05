from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    """Form for adding a new transaction."""
    class Meta:
        model = Transaction
        # The 'user' field will be set in the view, so it's excluded here
        fields = ['date', 'description', 'amount', 'transaction_type']
        
        # Add widgets to style the form fields to match your CSS
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date', 
                    'class': 'input-field'
                }
            ),
            'description': forms.TextInput(
                attrs={
                    'class': 'input-field', 
                    'placeholder': 'e.g., Salary, Groceries'
                }
            ),
            'amount': forms.NumberInput(
                attrs={
                    'class': 'input-field', 
                    'step': '0.01',
                    'placeholder': '0.00'
                }
            ),
            'transaction_type': forms.Select(
                attrs={
                    'class': 'input-field'
                }
            ),
        }
        labels = {
            'transaction_type': 'Type'
        }