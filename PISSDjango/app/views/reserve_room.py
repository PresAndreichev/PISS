from django.http import JsonResponse
from app.models import Room, RoomEvent, User
from django.views.decorators.csrf import csrf_exempt
from jwt import decode as jwt_decode, exceptions
from datetime import datetime
import json

reserved_rooms = []

@csrf_exempt
def reserve_room(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        
        token = data.get('token')
        room_id = data.get('room_id')
        date = data.get('date')
        start_time = data.get('startTime')
        end_time = data.get('endTime')
        topic = data.get('topic')

        if not all([token, room_id, date, start_time, end_time, topic]):
            return JsonResponse({"success": False, "message": "Missing required fields."}, status=400)

        role = 1  # Default to student
        user_id = None
        try:
            decoded_token = jwt_decode(token, options={"verify_signature": False})
            role = decoded_token.get('role', 1)
            user_id = decoded_token.get('user_id')
        except Exception as e:
            return JsonResponse({"success": False, "message": f"Invalid token: {str(e)}"}, status=400)

        try:
            date_obj = datetime.strptime(date.strip(), '%Y-%m-%d').date()
            start_time_obj = datetime.strptime(start_time.strip(), '%H:%M').time()
            end_time_obj = datetime.strptime(end_time.strip(), '%H:%M').time()
        except ValueError as e:
            return JsonResponse({"success": False, "message": f"Invalid date/time format: {str(e)}"}, status=400)

        if start_time_obj >= end_time_obj:
            return JsonResponse({"success": False, "message": "Start time must be before end time."}, status=400)



        overlapping_events = RoomEvent.objects.filter(
            room_id=room_id,
            date=date_obj,
            start_time__lt=end_time_obj,
            end_time__gt=start_time_obj,
        )
        # Check too see if all the events can be overriden
        for event in overlapping_events:
            host_priority = event.host.priority 
            if host_priority == 2: # Teacher attempting to book, can override
                return JsonResponse({
                    "success": False,
                    "message": "Room is already booked by a teacher during the selected time."
                }, status=400)

            if role == 1:  # Student attempting to book, cannot override other students
                return JsonResponse({
                    "success": False,
                    "message": "Room is already booked by another student during the selected time."
                }, status=400)

            if role == 2 and host_priority == 1:  # Teacher overriding a student
                # NB! Add notifier here later -> it will send info to the student was host or was attendant 
                event.delete() 

        try:
            room_event = RoomEvent.objects.create(
                room_id=room_id,
                date=date_obj,
                start_time=start_time_obj,
                end_time=end_time_obj,
                host_id=user_id,
                topic=topic
            )
            return JsonResponse({"success": True, "message": "Room successfully reserved.", "room_event_id": room_event.id}, status=200)
        except Exception as e:
            return JsonResponse({"success": False, "message": f"Error creating room event: {str(e)}"}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)