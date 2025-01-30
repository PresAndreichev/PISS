#event koito ne e lesson event, kato shte podava start_time, end_time, date, host_ID/or not, room_id/not
# get_meeting.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import RoomEvent, LessonEvent
import json

@csrf_exempt
def get_meeting(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            start_time = data.get('start_time')
            end_time = data.get('end_time')
            date = data.get('date')
            host_id = data.get('host_id')
            room_id = data.get('room_id')

            if not all([start_time, end_time, date]):
                return JsonResponse({"error": "start_time, end_time, and date are required."}, status=400)

            # Filter RoomEvent excluding LessonEvent
            events = RoomEvent.objects.exclude(id__in=LessonEvent.objects.values('id'))

            # Apply filters for time range and date
            events = events.filter(date=date, start_time__gte=start_time, end_time__lte=end_time)

            # Apply optional filters for host and room if provided
            if host_id:
                events = events.filter(host_id=host_id)
            if room_id:
                events = events.filter(room_id=room_id)

            # Serialize the event data to return as JSON
            event_data = [
                {
                    "id": event.id,
                    "topic": event.topic,
                    "room": event.room.id,
                    "date": event.date,
                    "start_time": event.start_time,
                    "end_time": event.end_time,
                    "attendees": [attendee.id for attendee in event.attendees.all()],
                    "host": event.host.id if event.host else None,
                }
                for event in events
            ]

            return JsonResponse({"events": event_data}, safe=False)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)




