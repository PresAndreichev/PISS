from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from django.contrib.auth.decorators import login_required
import json
from ..models import LessonEvent, LectureType

@csrf_exempt
def get_lessons(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            start_date = parse_datetime(data.get("startDate"))
            end_date = parse_datetime(data.get("endDate"))
            lesson_name = data.get("lessonName", "").strip()
            lesson_type = data.get("lessonType", "").strip()
            
            if not start_date or not end_date:
                return JsonResponse({"error": "Invalid start or end date"}, status=400)
            
            lessons = LessonEvent.objects.filter(date__range=[start_date.date(), end_date.date()])
            
            if lesson_name:
                lessons = lessons.filter(subject__name__icontains=lesson_name)
            
            if lesson_type:
                lessons = lessons.filter(lecture_type__type__iexact=lesson_type)
            
            lessons_data = [
                {
                    "id": lesson.id,
                    "lessonName": lesson.subject.name,
                    "roomNumber": lesson.room.id,
                    "date": lesson.date.strftime("%Y-%m-%d"),
                    "startTime": lesson.start_time.strftime("%H:%M"),
                    "endTime": lesson.end_time.strftime("%H:%M"),
                    "lectureType": lesson.lecture_type.type,
                }
                for lesson in lessons
            ]
            
            return JsonResponse({"lessons": lessons_data}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)