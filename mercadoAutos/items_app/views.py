from django.shortcuts import render, redirect
from .models import Item, FavoriteItem
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.core.mail import send_mail
from django.conf.global_settings import EMAIL_HOST_USER

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
    #@login_required(login_url='/auth/login/')
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