from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from tokens import decode_token

@csrf_exempt  # Use CSRF protection in production
@login_required  # Ensure the user is logged in
def disable_profile(request):
    if request.method == "POST":
        token = request.headers.get("Authorization").replace("Bearer ", "")
        user_id = decode_token(token)
        if not user_id:
            return JsonResponse({"success": False, "message": "Invalid token"}, status=401)
        
        try:
            user = request.user  # Get the currently logged-in user - potencialno se burka mejdu nashiq i django user-a
            user.is_profile_disabled = True
            user.save()

            return JsonResponse({"success": True, "message": "Profile disabled successfully"})

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)

