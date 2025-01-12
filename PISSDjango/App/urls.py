from django.urls import path
from .views.login import login_view
from .views.register import register_user
from .views.disable_profile import disable_profile
from .views.change_password import change_password
from .views.serve_html import serve_html

urlpatterns = [
    path('login/', login_view, name='login'),                        # Login route
    path('disable-profile/', disable_profile, name='disable_profile'),  # Disable profile route
    path('change_password/', change_password, name='change_password'),  # Room schedule route
    path('register/', register_user, name='register'),
    path('index/',lambda request: serve_html(request, 'index'),name='index'), 
    path('', lambda request: serve_html(request, 'register'), name='register'),  # Homepage route
]