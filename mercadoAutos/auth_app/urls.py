from django.urls import path, include
from .views import logout_view, login_view, signup_view, forgot_password, verification_code, change_username, change_email
urlpatterns = [
    path('login/', login_view.as_view(), name="Login"),
    path('logout/', logout_view, name="Logout"),
    path('signup/', signup_view.as_view(), name="Signup"),
    path('forgot/', forgot_password.as_view(), name="Forgot"),
    path('mail/', verification_code.as_view(), name="Verify"),
    path('username/', change_username.as_view(), name='SetName'),
    path('useremail/', change_email.as_view(), name='SetEmail'),
]