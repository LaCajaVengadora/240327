from django.shortcuts import render, redirect
from .models import Item, FavoriteItem
from django.contrib.auth.decorators import login_required

# Create your views here.
def item_view(request, id):
    item = Item.objects.get(ID=id)
    return render(request, 'item.html', {'item':item})

@login_required(login_url='/auth/login/')
def add_fav(request, id):
    item = Item.objects.get(ID=id); user = request.user

    if user.fav_items.filter(ID=item.ID).exists(): 
        FavoriteItem.objects.get(item=item, user=user).delete()
    else: 
        FavoriteItem(user=user, item=item).save()
    return redirect(request.META.get('HTTP_REFERER'))