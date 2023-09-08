from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Advertisements81, User
from .forms import Advertisements81Form
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.db.models import Count


def index(request):
    title = request.GET.get('query')
    if title:
        advertisements = Advertisements81.objects.filter(title__icontains=title)
    else:
        advertisements = Advertisements81.objects.all()
    context = {'advertisements':advertisements,
               'title':title,
               }
    return render(request, 'app_advertisements81/index.html', context)

def top_sellers(request):
    users = User.objects.annotate(
        adv_count = Count('advertisements81')
    ).order_by('-adv_count')
    context = {
        'users':users
    }
    return render(request, 'app_advertisements81/top-sellers.html', context)

@login_required(login_url=reverse_lazy('login'))
def advertisement_post(request):
    if request.method == "POST": # если нам что-то послали
        form = Advertisements81Form(request.POST, request.FILES) # получаем присланный текст и файлы
        if form.is_valid(): # если форма правильная
            new_advertisement = form.save(commit=False)
            new_advertisement.user = request.user # информация об отправителе - пользователе
            new_advertisement.save() # сохраняем
            url = reverse('main-page') # создаём ссылку на начальную страницу
            return HttpResponseRedirect(url) # и отправляем пользователя по ней
    else: # если нам ничего не посылали
        form = Advertisements81Form() # просто смотрим на форму
    context = {'form' : form}
    return render(request, 'app_advertisements81/advertisement-post.html', context)

def advertisememnt_detail(request, pk):

    advertisement = Advertisements81.objects.get(id=pk)
    context = {
        'advertisement':advertisement
    }
    return render(request, 'app_advertisements81/advertisement.html', context)