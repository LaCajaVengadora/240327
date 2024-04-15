from django import forms
from .models import Item, ItemImage

class ItemForm(forms.ModelForm):
    images = forms.ImageField(label='Imágenes', required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model = Item; fields = ['ID', 'marca', 'modelo', 'desc', 'price', 'category']

    def save(self, request, option):
        
        ID = self.cleaned_data.get('ID'); marca = self.cleaned_data.get('marca'); modelo = self.cleaned_data.get('modelo')
        desc = self.cleaned_data.get('desc'); price = self.cleaned_data.get('price'); 
        category = self.cleaned_data.get('category'); images = self.cleaned_data.get('images')
        user = request.user

        if option == 'CREATE':
            new_item = Item(ID=ID, marca=marca, modelo=modelo, desc=desc, price=price, author=user)
            new_item.save()
            for c in category: new_item.category.add(c)
            
            if images:
                for img in images: ItemImage.objects.create(item=new_item, img=img)
            else: ItemImage.objects.create(item=new_item)

            return new_item
        elif option == 'EDIT':
            item = Item.objects.get(ID=ID)
            item.marca=marca;item.modelo=modelo;item.desc=desc;item.price=price
            item.category.set(category)
            item.save(); return item

    
    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['ID'].widget.attrs.update({'class': 'form-control ', 'placeholder': 'Patente'})
        self.fields['marca'].widget.attrs.update({'class': 'form-control ', 'placeholder': 'Marca'})
        self.fields['modelo'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Modelo'})
        self.fields['desc'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Descripción'})
        self.fields['price'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Precio (en dólares)'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['images'].widget.attrs.update({'class': 'form-control'})
        self.fields['category'].label='Categorías'

