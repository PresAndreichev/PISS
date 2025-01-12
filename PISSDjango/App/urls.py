from django.urls import path
from App.views.login import login_view
from App.views.register import register_view
from App.views.disable_profile import disable_profile
from App.views.change_password import change_password

urlpatterns = [
    path('login/', login_view, name='login'),                        # Login route
    path('disable-profile/', disable_profile, name='disable_profile'),  # Disable profile route
    path('change_password/', change_password, name='change_password'),  # Room schedule route
    path('register/', register_view , name='register'),
]