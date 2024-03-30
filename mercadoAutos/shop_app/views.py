from django.shortcuts import render
from django.core.paginator import Paginator
from items_app.models import Item, ItemImage, Category

# Create your views here.
def test(request): return render(request, 'base.html')

def shop_view(request): return get_items(request)
def cat_view(request, cat): return get_items(request, cat)

def get_items(rq, cat = None):    

    if cat is not None: paginator = Paginator(Item.objects.filter(category__name=cat).order_by('-price'), 12)
    else: paginator = Paginator(Item.objects.all().order_by('-price'), 12)
    # con Paginator, teniendo all items, divide cada 12 items por pag
    pag_num = rq.GET.get('page', 1) # Obtiene num de pag del request, por defecto da 1
    items = paginator.get_page(pag_num) # Devuelve la pag con sus items

    cats = Category.objects.all()

    return render(rq, 'home.html', {'items':items,'cats':cats})