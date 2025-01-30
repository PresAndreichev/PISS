from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from ..models import LessonEvent, Room, LectureType
from app.views.tokens import decode_token
from ..models import User
from django.http import HttpResponse

#sortiram po data i chas i vrushtam tip na dali si host ili ne
def index_visualization(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON format."}, status=400)
    
        token = data.get('token')
        if not token:
            return JsonResponse({"success": False, "message": "Token not provided."}, status=400)
        try:
            decoded_token = decode_token(token)
            user_id = decoded_token.get('user_id')
        except Exception:
            return JsonResponse({"success": False, "message": "Invalid token provided."}, status=400)

        lesson_events = LessonEvent.objects.filter(attendees=user_id) | LessonEvent.objects.filter(host=user_id)

        lesson_events = lesson_events.order_by("date", "start_time")

        rooms = Room.objects.filter(events__in=lesson_events).distinct()

        # Serialize Lesson Events
        lessons_data = [
            {
                "id": lesson.id,
                "lessonName": lesson.subject.name,
                "roomId": lesson.room.id,
                "date": lesson.date.strftime("%Y-%m-%d"),
                "startTime": lesson.start_time.strftime("%H:%M"),
                "endTime": lesson.end_time.strftime("%H:%M"),
                "lectureType": lesson.lecture_type.type,
                "hostId": lesson.host.id if lesson.host else None,
                "hostName": lesson.host.full_name if lesson.host else "Unknown",
            }
            for lesson in lesson_events
        ]

        rooms_data = [
            {
                "id": room.id,
                "name": room.name,
                "capacity": room.capacity,
            }
            for room in rooms
        ]

        return JsonResponse({"rooms": rooms_data, "lessonEvents": lessons_data}, status=200)

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)