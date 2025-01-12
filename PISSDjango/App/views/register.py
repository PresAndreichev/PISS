from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from App.models import User
import json

@csrf_exempt
def register_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")

            # All required fields are filled?
            if not username or not email or not password:
                return JsonResponse({"success": False, "message": "Missing fields"}, status=400)

            # User already exists?
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                # Return success for security reasons but do not create a new user
                return JsonResponse({"success": True, "message": "User registration successful"},status=200)

            # Create a new user
            User.objects.create_user(
                username=username,
                email=email,
                password=make_password(password),  # hashes the password
                priority=0,  # admin can change it later to something else for teachers
                is_profile_disabled=False
            )

            return JsonResponse({"success": True, "message": "User registration successful"},status=200)
        except Exception as e:  # an exception has occurred withing the program, return it to the user
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    # Method not allowed
    return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)
