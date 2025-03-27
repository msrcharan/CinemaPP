# In forms.py of your app
from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm
    
from django.contrib.auth.forms import PasswordResetForm

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'placeholder': 'Re-enter password'}))
    receive_promotions = forms.BooleanField(
        label='Receive Promotions (check to register, uncheck to unregister)',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'checkbox-input'}),
    )

    class Meta:
        model = User
        fields = ['username', 'first_name','last_name','email', 'password', 'confirm_password','photo', 'address','phone_number','receive_promotions','credit_card_number','credit_card_expiry', 'credit_card_cvv']

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'confirm_password': forms.PasswordInput(attrs={'placeholder': 'Re-enter password'}),
            'address': forms.Textarea(attrs={'placeholder': 'Address'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone number'}),
            'credit_card_number': forms.TextInput(attrs={'placeholder': 'Credit Card Number'}),
            'credit_card_expiry': forms.TextInput(attrs={'placeholder': 'Expiry'}),
            'credit_card_cvv': forms.TextInput(attrs={'placeholder': 'CVV'}),
            # 'receive_promotions':forms.CheckboxInput(attrs={'placeholder': 'Receive Promotions'}),
        }
        labels = {
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'photo': 'Photo',
            'address': 'Address',
            'phone_number': 'Phone Number',
            'credit_card_number': 'Credit Card Number',
            'credit_card_expiry': 'Credit Card Expiry',
            'credit_card_cvv': 'Credit Card Cvv',
        }
    
    # photo = forms.ImageField(label='Photo', required=False)
    
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        return confirm_password
    
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
class UserLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(label='Remember Me', required=False)
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Password'})


class EditProfileForm(forms.ModelForm):
    receive_promotions = forms.BooleanField(
        label='Receive Promotions (check to register, uncheck to unregister)',
        required=False,
    )


    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['readonly'] = True

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'photo', 'address', 'phone_number', 'receive_promotions']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'address': forms.Textarea(attrs={'placeholder': 'Address'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone number'}),
            # 'receive_promotions':forms.CheckboxInput(attrs={'placeholder': 'Receive Promotions'}),
        }
        labels = {
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'photo': 'Photo',
            'address': 'Address',
            'phone_number': 'Phone Number',
            'receive_promotions': 'Receive Promotions',
        }

class EditPaymentForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['credit_card_number', 'credit_card_expiry', 'credit_card_cvv',
                  'credit_card_number_2', 'credit_card_expiry_2', 'credit_card_cvv_2',
                  'credit_card_number_3', 'credit_card_expiry_3', 'credit_card_cvv_3'
                  ]

class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder': 'Email address'})

class TicketForm(forms.Form):
    adult_tickets = forms.IntegerField(label='Number of Adult Tickets', min_value=0, initial=0)
    child_tickets = forms.IntegerField(label='Number of Child Tickets', min_value=0, initial=0)
    senior_tickets = forms.IntegerField(label='Number of Senior Citizen Tickets', min_value=0, initial=0)