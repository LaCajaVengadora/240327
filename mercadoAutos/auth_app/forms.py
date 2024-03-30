from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User

class UserCreationWithMailForm(UserCreationForm):
    email = forms.EmailField(label=False, required=True)

    class Meta:
        model = User; fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationWithMailForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit: user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(UserCreationWithMailForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})

        for field_name, field in self.fields.items(): field.label = False


class AuthenticationRemindForm(AuthenticationForm):
    remember_me = forms.BooleanField(label='Recordar', required=False)
    
    class Meta:
        model = User
        fields = ("username", "password", "remember_me")

    def __init__(self, *args, **kwargs):
        super(AuthenticationRemindForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control colspan-2', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control ', 'placeholder': 'Password'})
        self.fields['remember_me'].widget.attrs.update({'class': 'mt-2'})

        for field_name, field in self.fields.items(): 
            if field.label!='Recordar': field.label = False