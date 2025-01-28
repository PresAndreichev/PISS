from django.http import JsonResponse
from app.models import Room, RoomEvent
from datetime import datetime
import json

def filter_rooms(room_type, must_have_white_board, must_have_black_board, must_have_interactive_board, must_have_media):
    """With all available rooms, filter them by characteristics (!NB!) - this cannot be done in the DB, since we use BITS"""

    # Get all rooms which are not in repair
    available_rooms = [room for room in available_rooms if room.does_function()]

    match room_type:
        case 1:  # !In this parallel universe, students are allowed to used the PC rooms
            available_rooms = [room for room in available_rooms if room.is_computer_room()]
        case 2:
            available_rooms = [room for room in available_rooms if not room.is_computer_room()]
        # if 0, every room type is fine
        
    # The below are soft constraints - only if the host requires them, they will filter the room list
    # If he does not, he may still get a room with the following characteristics
    if must_have_white_board:
        available_rooms = [room for room in available_rooms if room.has_white_board()]
    if must_have_black_board:
        available_rooms = [room for room in available_rooms if room.has_black_board()]
    if must_have_interactive_board:
        available_rooms = [room for room in available_rooms if room.has_interactive_board()]
    if must_have_media:
        available_rooms = [room for room in available_rooms if room.has_media()]
    return available_rooms
 

def get_free_rooms(request):
    if request.method == 'POST':
        data = json.loads(request.body)
 
        # maybe sent the token here to extract the role and not sent it otherwise?
        # if no token, you are student
        role = data.get('role')  # Role: 1 (Student) or 2 (Teacher)
        date = data.get('date')  # Format: 'YYYY-MM-DD'
        start_time = data.get('startTime')  # Format of time: 'HH:MM'
        end_time = data.get('endTime')
        room_type = data.get('isComputer', 0) # 0 for either, 1 for pc, 2 for non
        must_have_white_board = data.get('hasWhiteBoard', False)
        must_have_black_board = data.get('hasBlackBoard', False)
        must_have_interactive_board = data.get('hasInteractiveBoard', False)
        must_have_media = data.get('hasMedia', False)
        min_capacity = data.get('minCapacity', 25)
 
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            start_time_obj = datetime.strptime(start_time, '%H:%M').time()
            end_time_obj = datetime.strptime(end_time, '%H:%M').time()
        except ValueError:
            return JsonResponse({"success": False, "message": "Invalid date or time format."}, status=400)
 
        # Find the overlapping roomEvents

        available_rooms = Room.objects.filters(
            seats__gte=min_capacity,
        ).exclude( # Exclude events which
            id__in=RoomEvent.objects.filter(
                date__eq=date_obj,
                start_time__lt=end_time_obj,  # Event starts before the searched time
                end_time__gt=start_time_obj,  # And Event ends after the searched time
                host__priority__gte=role  # And whose role is greater than ours
            ).values_list('room_id', flat=True)
        )
        # Even though we don't explicitly search for the hour, we will get all rooms (including in this timeslot)
        # And just exclude the ones with teacher's bookings during it
        
        available_rooms = filter_rooms(
            room_type, must_have_white_board, must_have_black_board,
            must_have_interactive_board, must_have_media
            )
 
        result = [
            {
                "id": room.id,
                "roomNumber": room.number,
                "floor": room.floor.id,
                "seats": room.seats,
                "isComputer": room.is_computer_room(),
                "hasWhiteBoard": room.has_white_board(),
                "hasBlackBoard": room.has_black_board(),
                "hasInteractiveBoard": room.has_interactive_board(),
                "hasMedia": room.has_media()
            }
            for room in available_rooms
        ]

        return JsonResponse({"success": True, "rooms": result}, status=200)
 
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)