from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf.global_settings import EMAIL_HOST_USER


class UserCreationWithMailForm(UserCreationForm):
    email = forms.EmailField(label=False, required=True)

    class Meta: model = User; fields = ("username", "email", "password1", "password2")

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



class VerificationCodeForm(forms.Form):
    verification_code = forms.CharField(label=False, max_length=6)

    def send_code(self):
        CODE = get_random_string(length=6)
        self.request.session['CODE']=CODE

        send_mail(
            'Verification Code',
            f'Your verification code is: {CODE}',
            EMAIL_HOST_USER,
            [self.request.session.get('user_data')['email']],
            fail_silently=False,
        )

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop('request', None)

        super(VerificationCodeForm, self).__init__(*args, **kwargs)
        self.fields['verification_code'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Verification code'})



class AuthenticationRemindForm(AuthenticationForm):
    remember_me = forms.BooleanField(label='Recordar', required=False)
    
    class Meta: model = User; fields = ("username", "password", "remember_me")

    def __init__(self, *args, **kwargs):
        super(AuthenticationRemindForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control colspan-2', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control ', 'placeholder': 'Password'})
        self.fields['remember_me'].widget.attrs.update({'class': 'mt-2'})
        for field_name, field in self.fields.items(): 
            if field.label!='Recordar': field.label = False



class PasswordChangeForm(UserCreationForm):
    email = forms.EmailField(label=False, required=True)
    password1 = forms.CharField(label=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label=False, widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta): model = User; fields = ('email','password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control ', 'placeholder': 'New Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control ', 'placeholder': 'Confirm Password'})
        self.fields['email'].widget.attrs.update({'class': 'form-control ', 'placeholder': 'User email'})

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1"); password2 = cleaned_data.get("password2"); email = self.cleaned_data.get("email")
        
        if password1 and password2 and password1 != password2: raise forms.ValidationError("Passwords do not match")
        if not User.objects.filter(email=email).exists(): raise forms.ValidationError("This email is not associated with any user")
        return cleaned_data

    def save(self, commit=True):
        user = User.objects.get(email=self.cleaned_data.get("email"))
        user.set_password(self.cleaned_data.get("password1"))
        if commit: user.save()
        return user



class UsernameChangeForm(forms.Form):
    newUsername = forms.CharField(label=False, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nuevo username'}))
    class Meta: model = User; fields = ('newUsername')
    def save(self, request):
        user = request.user; user.username = self.cleaned_data.get("newUsername")
        user.save(); return user



class EmailChangeForm(forms.Form):
    newEmail = forms.EmailField(label=False, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Nuevo email'}))
    class Meta: model = User; fields = ('newEmail')