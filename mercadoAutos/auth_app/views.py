from django.shortcuts import render, redirect
from .forms import UserCreationWithMailForm, AuthenticationRemindForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views.generic import View

# Create your views here.
def logout_view(request): logout(request); return redirect('Shop')

class login_view(View):

    def get(self, request): return render(request, 'login.html', {'form':AuthenticationRemindForm()})

    def post(self, request): 
        f = AuthenticationRemindForm(request, request.POST)
        if f.is_valid():
            user = authenticate(username=f.cleaned_data.get('username'), password= f.cleaned_data.get('password'))
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
            user = f.save()
            login(request, user)
            return redirect('Shop')
        else:
            for msg in f.error_messages:
                messages.error(request, f.error_messages[msg])
            return render(request, 'signup.html', {'form':f})