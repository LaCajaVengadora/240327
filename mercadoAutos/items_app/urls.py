from django.urls import path, include
from .views import item_view, add_fav, del_item, ask_view, add_item, edit_item
urlpatterns = [
    path('<str:id>', item_view, name='Item'),
    path('addFav/<str:id>', add_fav, name='Fav'),
    path('ask/', ask_view, name='Ask'),
    path('delete/<str:id>', del_item, name='Del'),
    path('newItem/', add_item.as_view(), name='NewItem'),
    path('editItem/<str:id>', edit_item.as_view(), name="EditItem")
] 