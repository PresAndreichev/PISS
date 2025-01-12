from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings

def serve_html(request, page_name):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'App/Static/html', f"{page_name}.html")
        with open(file_path, 'r',encoding='utf-8') as file:
            return HttpResponse(file.read(),content_type="text/html")
    except FileNotFoundError:
        return HttpResponse("Homepage not found",status=404)