from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from App.models import User
import json


@csrf_exempt  # Disable CSRF for simplicity
def login_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")

            # Validate input
            if not email or not password:
                return JsonResponse({"success": False, "message": "Email and password are required"}, status=400)

            # Fetch the user by email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({"success": False, "message": "Invalid credentials"}, status=401)

            if not check_password(password, user.password):
                return JsonResponse({"success": False, "message": "Invalid credentials"}, status=401)

            # maybe change the url as well - generate homepage info based on this
            return JsonResponse({"success": True, "message": "Login successful", "user_id": user.id})

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    # Return 405 Method Not Allowed for non-POST requests
    return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)
