from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from items_app.models import Item
from mercadoAutos.themes import set_coral, set_blue, set_yellow
from django.views.generic import View

# Create your views here.
@login_required(login_url='/auth/login/')
def gral_view(request): return render(request, 'profileT/profileGral.html')

@login_required(login_url='/auth/login/')
def items_view(request): 
    user_items = Item.objects.filter(author=request.user)
    return render(request, 'profileT/profileItems.html', {'items': user_items})

@login_required(login_url='/auth/login/')
def fav_view(request):
    favs = request.user.fav_items.all()
    return render(request, 'profileT/profileFavs.html', {'items': favs})

@login_required(login_url='/auth/login/')
def config_view(request): return render(request, 'profileT/profileConfig.html')

def set_theme(request):
    functions = {'Y': set_yellow,'B': set_blue,'C': set_coral}
    selected = functions.get(request.GET.get('theme'))
    if selected: selected(request)
    return redirect(request.META.get('HTTP_REFERER'))