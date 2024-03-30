from django.urls import path, include
from .views import logout_view, login_view, signup_view
urlpatterns = [
    path('login/', login_view.as_view(), name="Login"),
    path('logout/', logout_view, name="Logout"),
    path('signup/', signup_view.as_view(), name="Signup")
]