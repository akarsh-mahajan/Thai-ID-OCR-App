from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.upload_id_card, name='upload_id_card'),
]