from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app.models import User
import json
from app.views.tokens import generate_token

@csrf_exempt  # Disable CSRF for simplicity
def login_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            #check password 
            password = data.get("password")
            username = data.get("username")
            print(password, username)
            # Validate input
            if not username or not password:
                return JsonResponse({"success": False, "message": "Username and password are required"}, status=400)

            # Fetch the user by email
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return JsonResponse({"success": False, "message": "Invalid credentials"}, status=401)
                   
            if not check_password(password, user.password):
                return JsonResponse({"success": False, "message": "Invalid credentials"}, status=401)

            token = generate_token(user.id, user.username, user.priority) 
            return JsonResponse({"success": True, "message": "Login successful", "token": token, "role": user.priority})

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    # Return 405 Method Not Allowed for non-POST requests
    return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)
