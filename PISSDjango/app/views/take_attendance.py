# i need only user id taken from the token, room_id, 
#i take user id from the js, from the token, room id from the json
#bug when adding the room i should add the host (lector) who made the room event 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from ..models import LessonEvent
from app.views.tokens import decode_token
from app.views import User

@csrf_exempt
def take_attendance(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON format."}, status=400)
    
        token = data.get('token')
        if token:
            try:
                decoded_token = decode_token(token)
                user_id = decoded_token.get('user_id')
            except Exception:
                print("Invalid token provided.")


        room_event_id = data.get('roomEventId')
        try:
            lesson = LessonEvent.objects.get(id=room_event_id)
        except LessonEvent.DoesNotExist:
            return JsonResponse({"success": False, "message": "Lesson not found."}, status=404)
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"success": False, "message": "User not found."}, status=404)
        
        if user_id in lesson.attendees.all():
            return JsonResponse({"success": False, "message": "User already in attendance."}, status=400)
        
        lesson.attendees.add(user)
        lesson.save()
        return JsonResponse({"success": True, "message": "User added to attendance."}, status=200)
        
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)