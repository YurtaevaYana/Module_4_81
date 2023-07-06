from django.urls import path
from .views import index # подгрузили функцию index из файла views

urlpatterns = [
    path('', index) # дописали текстовый ответ к корневому пути (ссылке, которая появляется в терминале)
]