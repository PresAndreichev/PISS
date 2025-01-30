from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from django.db.models import Q
from ..models import RoomEvent, LessonEvent
import json
from app.views.tokens import decode_token

@csrf_exempt
def get_meetings(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)
           
    try:
        data = json.loads(request.body)
        start_date = parse_datetime(data.get("startDate"))
        end_date = parse_datetime(data.get("endDate"))

        if not all([start_date, end_date]):
            return JsonResponse({"error": "startDate and endDate are required fields!"}, status=400)
        query = Q(date__range=[start_date.date(), end_date.date()]) & ~Q(id__in=LessonEvent.objects.values("id"))
        # gets only the events which are in the given time period AND are not lesson events, just room events

        room_number = data.get('roomNumber')
        if room_number:
            query &= Q(room__number=room_number)

        token = data.get("token")
        if token:
            try:
                decoded_token = decode_token(token)
                user_id = decoded_token.get("user_id")
                query &= ~Q(attendees__id=user_id)  # Exclude events the user is already attending
                query &= ~Q(host_id=user_id)  # And exclude events the user is hosting
            except Exception:
                return JsonResponse({"error": "Provided token is not valid!"}, status=400)

        events = RoomEvent.objects.filter(query).order_by("date", "start_time", "end_time", "room_id")

        event_data = [
                {
                    "id": event.id,
                    "topic": event.topic,
                    "roomNumber": event.room.number,
                    "roomCapacity": event.room.seats,
                    "date": event.date,
                    "startTime": event.start_time,
                    "endTime": event.end_time,
                    "hostUsername": event.host.username,
                    "attendeesCount": len(event.attendees.all())
                }
                for event in events
            ]    

        return JsonResponse({"events": event_data}, safe=False)
    
    except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
    