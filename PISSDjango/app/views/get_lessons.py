from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from django.db.models import Q  # to use query set for more optimised querying!
#from django.contrib.auth.decorators import login_required
import json
from app.models import LessonEvent, LectureType

@csrf_exempt
def get_lessons(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
            data = json.loads(request.body)
            start_date = parse_datetime(data.get("startDate"))
            end_date = parse_datetime(data.get("endDate"))
            
            
            if not start_date or not end_date:
                return JsonResponse({"error": "No data range provided!"}, status=400)
            
            # Incrementally build a query but don't execute it yet
            query = Q(date__range=[start_date.date(), end_date.date()])
            print(start_date, end_date)

            lesson_name = data.get("lessonName", "").strip()
            print(lesson_name)
            if lesson_name:  # if a concrete lessons are provided, return only them!
                query &= Q(subject__name__icontains=lesson_name)

            lesson_type = data.get("lessonType", "").strip()
            print(lesson_type)
            if lesson_type and lesson_type != "All":
                query &= Q(lecture_type__type__iexact=lesson_type)

            # And finally now execute the completed query
            lessons = LessonEvent.objects.filter(query).order_by("date", "start_time", "end_time", "room_id")
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
    
    