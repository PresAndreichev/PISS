from django.urls import path
from .views.login import login_view
from .views.register import register_user
from .views.disable_profile import disable_profile
from .views.change_password import change_password
from .views.serve_html import serve_html
from .views.get_rooms import get_rooms
from .views.reserve_room import reserve_room
from .views.get_lessons import get_lessons
from .views.take_attendance import take_attendance
from .views.list_subjects import list_subjects
from .views.index_visualization import index_visualization
from .views.get_meetings import get_meetings
from .views.qr_scanner import qr_scanner

urlpatterns = [
    path('api/login/', login_view, name='login'),                        # Login route
    path('api/disable-profile/', disable_profile, name='disable_profile'),  # Disable profile route
    path('api/change_password/', change_password, name='change_password'),  # Room schedule route
    path('api/register/', register_user, name='register_user'),
    path('', lambda request: serve_html(request, 'main'), name='main'),  # Homepage route
    path('api/get_rooms/', get_rooms, name='get_rooms'),
    path('api/reserve_room/', reserve_room, name='reserve_room'),
    path('api/get_lessons/', get_lessons, name='get_lesson'),
    path('api/take_attendance/', take_attendance, name='take_attendance'),
    path('api/list_subjects/', list_subjects, name='list_subjects'),
    path('api/index_visualization/', index_visualization, name='index_visualization'),
    path('api/get_meetings/', get_meetings, name='get_meetings'),
    path('api/qr_scanner/', qr_scanner, name ='qr_scanner')
]
# Add the URLS, of the get_lesson, take_attendance, get_rooms, reserve_room, get_saved_rooms