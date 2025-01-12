from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def serve_html(request, page_name):
    try:
        with open(f'App/Static/html/{page_name}.html', 'r',encoding='utf-8') as file:
            return HttpResponse(file.read(),content_type="text/html")
    except FileNotFoundError:
        return HttpResponse("Homepage not found",status=404)