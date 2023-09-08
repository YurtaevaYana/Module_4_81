from django.urls import path
from .views import index, top_sellers, advertisement_post, advertisememnt_detail

urlpatterns = [
    path('', index, name='main-page'),
    path('top-sellers/', top_sellers, name='top-sellers'),
    path('advertisement-post/', advertisement_post, name='adv-post'),
    path('advertisement/<int:pk>', advertisememnt_detail, name='adv-detail'),
]