#po azbuchen red predmeti 
# vrushtam ime, lessond_id
from django.http import HttpResponse
from django.shortcuts import render 
from app.models import Subject
from django.http import JsonResponse

def list_subjects(request):
    subjects = Subject.objects.all().order_by('name','id')

    subject_data = [{'subjects': subject.name, 'subject_id': subject.id  }
        for subject in subjects ]

    return JsonResponse({"subjects": subject_data}, status=200)