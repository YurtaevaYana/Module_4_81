from django.shortcuts import render
from django.http import HttpResponse

def lesson_4(request):
    return HttpResponse('Домашка по 4 заданию')