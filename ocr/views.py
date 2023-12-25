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
from . import utils


#views for handling thai id upload and data extraction
def upload_id_card(request):
    if request.method == 'POST':
        image_file = request.FILES['image']
        ocr_result = utils.process_ocr(image_file)
        context = {'ocr_data': ocr_result}
        return render(request, 'ocr_result.html', context)
    else:
        return render(request, 'upload.html')


#view to load previous executions   
def load_previous_executions(request):
    if request.method == 'GET':
        past_records = utils.get_previous_executions()
        # Pass previous_executions to the template
        context = {'previous_executions': past_records}
        return render(request, 'previous_executions.html', context)
    else:
        return render(request, 'previous_executions.html')    


#view to filter previous execution based on given parameters
def filter_previous_executions(request):
    if request.method == 'GET':
        date_of_issue_param = request.GET.get('date_of_issue', '')
        date_of_expiry_param = request.GET.get('date_of_expiry', '')
        date_of_birth_param = request.GET.get('date_of_birth', '')
        identification_no_param = request.GET.get('identification_number', '')
        name_param = request.GET.get('name', '')
        last_name_param = request.GET.get('last_name', '')
        filter_records = utils.filter_execution_records(date_of_expiry_param, date_of_issue_param, date_of_birth_param,
                                                  identification_no_param, name_param, last_name_param)
        context = {'filtered_records': filter_records}
        return render(request, 'filter_records.html', context)
    else:
        return render(request, 'filter_records.html')
    
#view to handle request to fetch and delete the record with the given identification number
def fetch_record(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'fetch':
            input_identification_no = request.POST.get('fetch_id_number', '')
            fetched_record = OcrRecord.objects.filter(identification_number=input_identification_no)
            context = {'fetched_record': fetched_record}
            if not fetched_record:
                messages.error(request, 'Requested Record not found.')
            return render(request, 'fetch_records.html', context)
        elif action == 'delete':
            input_identification_no = request.POST.get('fetch_id_number', '')
            record_to_delete = OcrRecord.objects.filter(identification_number=input_identification_no)
            deleted_records = {}
            context = {}
            if record_to_delete:
                deleted_records = copy.deepcopy(record_to_delete)
                context = {'fetched_record': deleted_records}
                record_to_delete.delete()
                messages.success(request, 'Record deleted successfully.')
            else:
                messages.error(request, 'Unable to delete record as requested record not found.')
            return render(request, 'fetch_records.html', context)
    else:
        return render(request, 'fetch_records.html')

