from django.urls import path, include
from .views import item_view, add_fav, ask_view
urlpatterns = [
    path('<str:id>', item_view, name='Item'),
    path('addFav/<str:id>', add_fav, name='Fav'),
    path('ask/', ask_view.as_view(), name='Ask')
] 