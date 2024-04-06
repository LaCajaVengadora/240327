from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from items_app.models import Item

# Create your views here.
@login_required(login_url='/auth/login/')
def gral_view(request): return render(request, 'profileGral.html')

@login_required(login_url='/auth/login/')
def items_view(request): 
    user_items = Item.objects.filter(author=request.user)
    print(user_items)
    return render(request, 'profileItems.html', {'items': user_items})

@login_required(login_url='/auth/login/')
def fav_view(request): return render(request, 'profileFavs.html')

@login_required(login_url='/auth/login/')
def config_view(request): return render(request, 'profileConfig.html')