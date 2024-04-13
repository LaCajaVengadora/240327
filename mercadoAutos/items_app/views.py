from django.shortcuts import render, redirect
from .models import Item, FavoriteItem
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.core.mail import send_mail
from django.contrib import messages
from django.conf.global_settings import EMAIL_HOST_USER
from .forms import NewItemForm

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

class ask_view(View):
    def get(self, request): return redirect('Shop')
    def post(self, request):
        offererEmail = request.POST.get('offererEmail'); consulta = request.POST.get('consulta')
        if not request.user.is_authenticated: return redirect('Login')
        send_mail(
            f'{request.user.username} ha consultado por tu producto!',
            f'{consulta}\n\nPuedes contactar a {request.user.username} en {request.user.email}',
            EMAIL_HOST_USER,
            [offererEmail],
            fail_silently=False,
        )
        return render(request, 'success.html')

def del_item(request, id):
    if request.method=='POST': Item.objects.get(ID=id).delete()
    return redirect('MyItems')

class add_item(View):
    def get(self, request):
        if not request.user.is_authenticated: return redirect('Login')
        return render(request,'newItem.html',{'form':NewItemForm()})
    def post(self, request):
        f = NewItemForm(request.POST)
        if f.is_valid():
            f.save(request)
            return redirect('MyItems')
        for field, errors in f.errors.items():
            for error in errors: messages.error(request, f"{field}: {error}")
        return render(request, 'newItem.html', {'form':f})