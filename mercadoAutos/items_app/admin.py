from django.contrib import admin
from .models import Item, ItemImage, Category
from django.utils.translation import gettext_lazy as _
# Register your models here.
class HasItems(admin.SimpleListFilter):
    title = _('Has items')
    parameter_name = 'has_items'
    def lookups(self, request, model_admin): return [('yes', 'Yes'),('no', 'No')]
    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(name__in=Item.objects.values('category').distinct())
        elif self.value() == 'no':
            return queryset.exclude(name__in=Item.objects.values('category').distinct())
class PriceOrder(admin.SimpleListFilter):
    title = _('Price (US$)')
    parameter_name = 'price_order'
    def lookups(self, request, model_admin): 
        return [('10', '< 10.000'),('25', '10.000 ~ 25.000'), ('50', '25.000 ~ 50.000'), ('^', '50.000 <')]
    def queryset(self, request, queryset):
        if self.value() == '10': return queryset.filter(price__lte=10000.0)
        elif self.value() == '25': return queryset.filter(price__gte=10000.0, price__lte=25000.0)
        elif self.value() == '50': return queryset.filter(price__gte=25000.0, price__lte=50000.0)
        elif self.value() == '^': return queryset.filter(price__gte=50000.0)

class CategoriAdmin(admin.ModelAdmin):
	list_display = ['name', 'color']; search_fields = list_display; list_filter=[HasItems]

class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'display_category', 'display_author_username']
    search_fields = ['number', 'name', 'price', 'category__name']
    list_filter = ['category', PriceOrder]
    def display_category(self, obj): return " - ".join([c.name for c in obj.category.all()])
    display_category.short_description = 'Categories'
    def display_author_username(self, obj): return obj.author.username
    display_author_username.short_description = 'Author'

class ImageAdmin(admin.ModelAdmin):
    list_display = ['ID', 'display_item', 'img']
    search_fields = ['ID', 'item_name', 'img']
    def display_item(self, obj): return obj.item.name
    display_item.short_description = 'Item name'

admin.site.register(Category, CategoriAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemImage, ImageAdmin)