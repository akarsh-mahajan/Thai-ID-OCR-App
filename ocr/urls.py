from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.upload_id_card, name='upload_id_card'),
    path('records/', views.load_previous_executions, name='load_previous_executions'),
    path('filter/', views.filter_previous_executions, name='filter_previous_executions'),
    path('fetch_record/', views.fetch_record, name='fetch_record'),
]