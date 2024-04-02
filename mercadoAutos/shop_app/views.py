from django.shortcuts import render
from django.core.paginator import Paginator
from items_app.models import Item, ItemImage, Category
from django.db.models import Q

# Create your views here.
def test(request): return render(request, 'base.html')

def shop_view(request): return get_items(request)
def cat_view(request, cat): return get_items(request, cat)

def get_items(request, cat = None):    

    query = request.GET.get('q'); raw_items = Item.objects.all()

    if cat: raw_items = raw_items.filter(category__name=cat)
    if query: 
        raw_items = raw_items.filter(
            Q(ID__icontains=query) | Q(marca__icontains=query) | Q(modelo__icontains=query)
        )

    paginator = Paginator(raw_items.order_by('-price'), 12)# con Paginator, teniendo los items, divide cada 12 items por pag
    pag_num = request.GET.get('page', 1) # Obtiene num de pag del request, por defecto da 1
    items = paginator.get_page(pag_num) # Devuelve la pag con sus items
    
    cats = Category.objects.all()

    return render(request, 'home.html', {'items':items,'cats':cats})