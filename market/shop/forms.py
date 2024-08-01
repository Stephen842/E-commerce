from django import forms
from .models import Customer, Products, Order

 #this below works for the administrative uploading of properties       
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Name'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 8:
            raise forms.ValidationError('Name must be 8 characters long or more')
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if len(email) < 8:
            raise forms.ValidationError('Email address must be 8 characters long')
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError('Email Address Already Registered...')
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) < 8:
            raise forms.ValidationError('Phone number is too short')
        return phone

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError('Password is too short')
        return password
    
class SigninForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}))
    
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Name'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter PAssword'}),
        }

