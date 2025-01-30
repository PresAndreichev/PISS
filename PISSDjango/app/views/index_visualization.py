from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from ..models import LessonEvent
from app.views.tokens import decode_token
from ..models import User
from django.http import HttpResponse

def index_visualization(request):
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

        

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)