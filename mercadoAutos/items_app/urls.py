from django.urls import path, include
from .views import item_view, add_fav
urlpatterns = [
    path('<str:id>', item_view, name='Item'),
    path('addFav/<str:id>', add_fav, name='Fav'),
] 