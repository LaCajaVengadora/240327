from django.urls import path, include
from .views import gral_view, items_view, fav_view, config_view, set_theme
urlpatterns = [
    path('gral/', gral_view, name='Profile'),
    path('my-items/', items_view, name='MyItems'),
    path('fav-items/', fav_view, name='MyFav'),
    path('config/', config_view, name='Config'),
    path('setTheme/', set_theme, name='Theme')
] 