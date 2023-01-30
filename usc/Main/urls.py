from django.urls import path

from . import views


app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.full_text_search, name='search'),
]
