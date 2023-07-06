from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse('Успешно!') # возвращаем текст "Успешно!" в качестве ответа на странице