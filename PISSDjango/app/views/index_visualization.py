from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Q
from ..models import LessonEvent, RoomEvent
from app.views.tokens import decode_token


def extract_unique_room_events_for_user(lesson_events, user_id):
    """Get the Room Events where the user is a host OR an attendee, so they aren't from the above collection"""
    lesson_event_ids = lesson_events.values_list("id", flat=True)
    room_events = (
        RoomEvent.objects.filter(Q(attendees=user_id) | Q(host=user_id))
        .exclude(id__in=lesson_event_ids)
    )

    return [
        {
            "id": event.id,
            "roomNumber": event.room.number,
            "date": event.date.strftime("%Y-%m-%d"),
            "startTime": event.start_time.strftime("%H:%M"),
            "endTime": event.end_time.strftime("%H:%M"),
            "hostUserName": event.host.username,
            "attendeesCount": event.attendees.count(),
            "totalSeats": event.room.seats,
            "topic": event.topic
        }
        for event in room_events
    ]


@csrf_exempt
def index_visualization(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)
    
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

    # Lessons where user is host or attendee
    lesson_events = LessonEvent.objects.filter(Q(attendees=user_id) | Q(host=user_id))
    room_events = extract_unique_room_events_for_user(lesson_events, user_id)
    
    lesson_events = [
        {
            "id": lesson.id,
            "roomNumber": lesson.room.number,
            "date": lesson.date.strftime("%Y-%m-%d"),
            "startTime": lesson.start_time.strftime("%H:%M"),
            "endTime": lesson.end_time.strftime("%H:%M"),
            "hostUserName": lesson.host.username,
            "attendeesCount": lesson.attendees.count(),
            "totalSeats": lesson.room.seats,
            "topic": lesson.topic,
            "subjectName": lesson.subject.name,
            "lectureType": lesson.lecture_type.type,
        }
        for lesson in lesson_events
    ]

    # Order only the combined list, don't order the separate ones in order to optimize performance
    combined_events = sorted(lesson_events + room_events, 
                             key=lambda x: (x["date"], 
                                            x["startTime"], 
                                            x["endTime"], 
                                            x["attendeesCount"], 
                                            x["totalSeats"], 
                                            x["topic"]
                                            ))
    return JsonResponse({"events": combined_events}, status=200)