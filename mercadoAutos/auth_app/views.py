from django.shortcuts import render, redirect
from django.views.generic import View

from .forms import UserCreationWithMailForm, AuthenticationRemindForm, PasswordChangeForm, VerificationCodeForm
from django.contrib import messages

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User



# Create your views here.
def logout_view(request): logout(request); return redirect('Shop')


class login_view(View):

    def get(self, request): return render(request, 'login.html', {'form':AuthenticationRemindForm()})

    def post(self, request): 
        f = AuthenticationRemindForm(request, request.POST)
        if f.is_valid():

            user = authenticate(username=f.cleaned_data['username'], password= f.cleaned_data['password'])
            if user is not None:
                login(request, user)
                if f.cleaned_data.get('remember_me'): request.session.set_expiry(2592000)
                else: request.session.set_expiry(0)
                return redirect('Shop')
            
        for msg in f.error_messages:
            messages.error(request, f.error_messages[msg])
        return render(request, 'login.html', {'form':f})


class signup_view(View):

    def get(self, request): return render(request, 'signup.html', {'form':UserCreationWithMailForm()})

    def post(self, request):
        f = UserCreationWithMailForm(request.POST)
        if f.is_valid():

            request.session['user_data'] = {
                'user':f.cleaned_data['username'],
                'email':f.cleaned_data['email'],
                'pass':f.cleaned_data['password1'],
            }
            return redirect('Verify')
        
        for msg in f.error_messages:
            messages.error(request, f.error_messages[msg])
        return render(request, 'signup.html', {'form':f})


class verification_code(View):

    def get(self, request):
        f = VerificationCodeForm(request=request); f.send_code()
        return render(request, 'verification_code.html', {'form': f})

    def post(self, request):
        f = VerificationCodeForm(request.POST, request=request)
        if f.is_valid():

            entered_code = f.cleaned_data['verification_code']
            user_data = request.session.get('user_data')

            if entered_code == request.session.get('CODE'):
                user = User.objects.create_user(username=user_data['user'], email=user_data['email'], password=user_data['pass'])
                user.save()
                login(request, user)
                return redirect('Shop')
            else:
                return redirect('/auth/mail/?wrong')


class forgot_password(View):

    def get(self, request): return render(request, 'forgot_p.html', {'form':PasswordChangeForm()})

    def post(self, request):
        f = PasswordChangeForm(request.POST)
        if f.is_valid():
            user = f.save()
            login(request, user)
            return redirect('Shop')
        else:
            for msg in f.error_messages:
                messages.error(request, f.error_messages[msg])
            return render(request, 'forgot_p.html', {'form':f})