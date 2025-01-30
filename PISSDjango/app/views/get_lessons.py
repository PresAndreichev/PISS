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
            
            if not start_date or not end_date or not lesson_name or not lesson_type:
                return JsonResponse({"error": "Not a valid data"}, status=400)
            
            if lesson_type == "all":
                lessons = LessonEvent.objects.filter(subject__name__icontains=lesson_name, 
                                                    date__range=[start_date.date(), end_date.date()])
            else:
                lessons = LessonEvent.objects.filter(subject__name__icontains=lesson_name,
                                                    lecture_type__type__iexact=lesson_type, 
                                                    date__range=[start_date.date(), end_date.date()])
                
            lessons = sorted(lessons, key=lambda x: (x.date, x.start_time, x.end_time, x.room.id))
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