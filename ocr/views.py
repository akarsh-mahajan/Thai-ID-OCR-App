from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import OcrRecord
from google.cloud import vision
from google.cloud.vision_v1 import types
import json
from django.contrib import messages
from django.shortcuts import render
from django.http import request
import re
import copy
import datetime
from . import ocr_processor


#views for handling thai id upload and data extraction
def upload_id_card(request):
    if request.method == 'POST':
        image_file = request.FILES['image']
        ocr_result = ocr_processor.process_ocr(image_file)
        context = {'ocr_data': ocr_result}
        return render(request, 'ocr_result.html', context)
    else:
        return render(request, 'upload.html')


#view to load previous executions   
def load_previous_executions(request):
    if request.method == 'GET':
        past_records = get_previous_executions()
        # Pass previous_executions to the template
        context = {'previous_executions': past_records}
        return render(request, 'previous_executions.html', context)
    else:
        return render(request, 'previous_executions.html')    

def get_previous_executions():
    return OcrRecord.objects.all()

