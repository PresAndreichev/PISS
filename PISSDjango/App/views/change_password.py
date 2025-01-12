from django.contrib.auth.hashers import check_password, make_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from App.models import User
import json
from App.views.tokens import decode_token

@csrf_exempt  # Disable CSRF for simplicity
def change_password(request, user_id):
    if request.method == "POST":
        token = request.headers.get("Authorization").replace("Bearer ", "")
        user_id = decode_token(token)
        if not user_id:
            return JsonResponse({"success": False, "message": "Invalid token"}, status=401)



        try:
            data = json.loads(request.body)
            current_password = data.get("current_password")
            new_password = data.get("new_password")


            if not current_password or not new_password:
                return JsonResponse({"success": False, "message": "Missing required fields"}, status=400)

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                # note we return true and don't spoil if a user exists or not!
                return JsonResponse({"success": True, "message": "Password successfully updated"}, status=200)

            if not check_password(current_password, user.password):
                return JsonResponse({"success": False, "message": "Incorrect current password"}, status=401)

            user.password = make_password(new_password)
            user.save()

            return JsonResponse({"success": True, "message": "Password updated successfully"})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)
