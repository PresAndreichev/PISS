from django.http import JsonResponse, HttpResponse
from ..views.tokens import decode_token
import json, re
from django.views.decorators.csrf import csrf_exempt
from ..models import User,Student, RoomEvent

def validate_data_format(data):
    pattern = r"^[0-9]{1}MI[0-9]{7}$"
    return re.match(pattern, data)


@csrf_exempt
def qr_scanner(request):
    #priema event_id i token na prepodavatelq
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON format."}, status=400)

        token = data.get('token')
        qr_code = data.get('qr_code')
        if not token or not qr_code:
            return JsonResponse({"success": False, "message": "Missing token or QR code data."}, status=400)

        try:
            decoded_token = decode_token(token)
            user_id = decoded_token.get('user_id')
            role = decoded_token.get('role')
        except Exception:
            return JsonResponse({"success": False, "message": "Invalid token provided."}, status=400)

        # Ensure the user has the correct role (role == 2)
        if role != 2:
            return JsonResponse({"success": False, "message": "Insufficient role."}, status=403)

        if not validate_data_format(qr_code):
            return JsonResponse({"success": False, "message": "Invalid QR code format."}, status=400)
        
        try:
            student = Student.objects.get(faculty_num=qr_code)
        except Student.DoesNotExist:
            return JsonResponse({"success": False, "message": "Invalid faculty number."}, status=400)

        event_id = data.get('event_id')
        if not event_id:
            return JsonResponse({"success": False, "message": "Event ID is required."}, status=400)


        try:
            room_event = RoomEvent.objects.get(id=event_id)
        except RoomEvent.DoesNotExist:
            return JsonResponse({"success": False, "message": "Room event not found."}, status=404)

        user = student.user
        if user in room_event.attendees.all():
            return JsonResponse({"success": False, "message": "User already marked as attended."}, status=400)

        room_event.attendees.add(user)
        room_event.save()

        #print(f"User {user.username} added to event {room_event.topic}.")

        return JsonResponse({"success": True, "user": {user.username}}, status=200)

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)