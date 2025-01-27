from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app.models import User, Student
import json


@csrf_exempt
def register_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")
            priority = data.get("role")
            if priority == 2:
                faculty_num = None
            else:
                faculty_num=data.get("fn")
            # Validate required fields
            if not username or not email or not password or (priority == 1 and not faculty_num):
                return JsonResponse({"success": False, "message": "Missing fields"}, status=400)

            # Check if user already exists
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                return JsonResponse({"success": True, "message": "User registration successful"}, status=200)

            # Create a new user
            User.objects.create(
                username=username,
                email=email,
                password=make_password(password),
                priority=priority,
                is_profile_disabled=False
            )   
            if priority == "1":
                user = User.objects.get(username=username)
                Student.objects.create(
                    user=user,  # Bind the existing User instance
                    faculty_num=faculty_num
                )

            return JsonResponse({"success": True, "message": "User registration successful"}, status=200)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)
