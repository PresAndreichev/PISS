from django.urls import path
from .views.login import login_view
from .views.register import register_user
from .views.disable_profile import disable_profile
from .views.change_password import change_password
from .views.serve_html import serve_html
from .views.get_rooms import get_rooms
from .views.reserve_room import reserve_room


urlpatterns = [
    path('api/login/', login_view, name='login'),                        # Login route
    path('api/disable-profile/', disable_profile, name='disable_profile'),  # Disable profile route
    path('api/change_password/', change_password, name='change_password'),  # Room schedule route
    path('api/register/', register_user, name='register_user'),
    path('', lambda request: serve_html(request, 'main'), name='main'),  # Homepage route
    path('api/get_rooms/', get_rooms, name='get_rooms'),
    path('api/reserve_room/', reserve_room, name='reserve_room')
]
# Add the URLS, of the get_lesson, take_attendance, get_rooms, reserve_room, get_saved_rooms