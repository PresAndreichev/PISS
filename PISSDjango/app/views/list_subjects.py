from app.models import Subject
from django.http import JsonResponse

def list_subjects(request):
    subjects = Subject.objects.all().order_by('name','id')
    subject_data = [{'subjectName': subject.name, 'subjectId': subject.id  }
        for subject in subjects ]

    return JsonResponse({"subjects": subject_data}, status=200)