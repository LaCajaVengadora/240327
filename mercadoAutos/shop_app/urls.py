from django.urls import path, include
from .views import test, shop_view, cat_view
urlpatterns = [
    #path('', test)
    path('', shop_view, name="Shop"),
    path('<str:cat>', cat_view)
]