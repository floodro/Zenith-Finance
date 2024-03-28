from django import forms

class CreateNewAccount(forms.Form):
    first_name = forms.CharField(label="First Name", max_length=200)
    last_name = forms.CharField(label="Last Name", max_length=200)
    sr_code = forms.CharField(label="SR Code", max_length=8)
    campus = forms.CharField(label="Campus", max_length=200)
    
    