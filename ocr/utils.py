from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import OcrRecord
from google.cloud import vision
from google.cloud.vision_v1 import types
import json
from django.shortcuts import render
from django.http import request
import re
import datetime



def process_ocr(image):
    client = vision.ImageAnnotatorClient()
    with open(image.temporary_file_path(), 'rb') as image_file:
        content = image_file.read()
        vision_image = vision.Image(content=content)
        response = client.document_text_detection(image=image)
        ocr_result = extract_data_from_response(response)
        record = OcrRecord.objects.create(
            identification_number=ocr_result.get('Identification ID', ''),
            first_name=ocr_result.get('First Name', ''),
            last_name=ocr_result.get('Last Name', ''),
            date_of_birth=ocr_result.get('Date of Birth', None),
            date_of_issue=ocr_result.get('Date of Issue', None),
            date_of_expiry=ocr_result.get('Date of Expiry', None),
            status=ocr_result.get('status', 'failure'),  # Set default status
            error_message=ocr_result.get('reason')
        )
        result = get_ui_response(record)
    return result


def extract_data_from_response(response):
    ocr_result = {}
    text_annotations = response.text_annotations
    # Extract relevant fields based on their labels or patterns
    for text_annotation in text_annotations:
        text = text_annotation.description.strip().lower()
        status = True
        reason = ''
        ocr_result, status, reason = get_id_number(text, ocr_result, status, reason)
        ocr_result, status, reason = get_name(text, ocr_result, status, reason)
        ocr_result, status, reason = get_last_name(text, ocr_result, status, reason)
        ocr_result, status, reason = get_date_of_birth(text, ocr_result, status, reason)
        ocr_result, status, reason = get_date_of_issue(text, ocr_result, status, reason)
        ocr_result, status, reason = get_date_of_expiry(text, ocr_result, status, reason)
        ocr_result['status'] = 'success' if status is True else 'failure'
        ocr_result['reason'] = reason if status is False else ''
        return ocr_result
    
def get_id_number(text, ocr_result, status, reason):
    id_no = re.search(r'\d{1}\s\d{4}\s\d{5}\s\d{2}\s\d', text)
    try:
        if id_no:
            ocr_result['Identification ID'] = id_no.group(0)
        else:
            status = False
            reason = 'Unable to extract ID number.'
    except Exception as e:
        status = False
        reason = 'Unable to extract ID number.'
    return ocr_result, status, reason


def get_name(text, ocr_result, status, reason):
    name = re.search(r'name (.+)', text)
    try:
        if name:
            ocr_result['First Name'] = name.group(1)
        else:
            status = False
            reason = 'Unable to extract name.'
    except Exception as e:
        status = False
        reason = 'Unable to extract name.'
    return ocr_result, status, reason


def get_last_name(text, ocr_result, status, reason):
    last_name = re.search(r'last name (.+)', text)
    try:
        if last_name:
            ocr_result['Last Name'] = last_name.group(1)
        else:
            status = False
            reason = 'Unable to extract last name.'
    except Exception as e:
        status = False
        reason = 'Unable to extract last name.'
    return ocr_result, status, reason


def get_date_of_birth(text, ocr_result, status, reason):
    dob = re.search(r'date of birth (.+)', text)
    try:
        if dob:
            dob_string = dob.group(1)
            ocr_result['Date of Birth'] = convert_to_date(dob_string)
        else:
            status = False
            reason = 'Unable to extract date of birth'
    except Exception as e:
        status = False
        reason = 'Unable to extract date of birth, possible reason can be that date is out of permissible range'
    return ocr_result, status, reason


def get_date_of_issue(text, ocr_result, status, reason):
    doi = re.search(r'(.+)\ndate of issue', text)
    try:
        if doi:
            doi_string = doi.group(1)
            ocr_result['Date of Issue'] = convert_to_date(doi_string)
        else:
            status = False
            reason = 'Unable to extract date of issue'
    except Exception as e:
        status = False
        reason = 'Unable to extract date of issue, possible reason can be that date is out of permissible range'
    return ocr_result, status, reason


def get_date_of_expiry(text, ocr_result, status, reason):
    doe = re.search(r'(.+)\ndate of expiry', text)
    try:
        if doe:
            doe_string = doe.group(1)
            ocr_result['Date of Expiry'] = convert_to_date(doe_string)
        else:
            status = False
            reason = 'Unable to extract date of expiry'
    except Exception as e:
        status = False
        reason = 'Unable to extract date of expiry, possible reason can be that date is out of permissible range'
    return ocr_result, status, reason


def convert_to_date(date_str):
    day, month_str, year = date_str.split()[:3]
    month_dict = {
        "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
        "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12
    }
    month = month_dict[month_str.strip(".").lower()]  # Remove the trailing period
    return datetime.date(int(year), month, int(day))


def get_ui_response(record: OcrRecord):
    ui_response = {
        'identification_number': record.identification_number,
        'first_name': record.first_name.upper(),
        'last_name': record.last_name.upper(),
        'date_of_birth': record.date_of_birth,
        'date_of_issue': record.date_of_issue,
        'date_of_expiry': record.date_of_expiry,
        'status': record.status,
        'error_message': record.error_message
    }
    return ui_response

def get_previous_executions():
    return OcrRecord.objects.all()

def filter_execution_records(date_of_expiry_param, date_of_issue_param, date_of_birth_param, identification_no_param,
                             name_param, last_name_param):
    results = OcrRecord.objects.all()
    # YYYY-MM-DD --> python.date
    if date_of_birth_param != '':
        results = results.filter(date_of_birth=datetime.datetime.strptime(date_of_birth_param, '%Y-%m-%d').date())

    if date_of_issue_param != '' and date_of_expiry_param != '':
        results = results.filter(
            date_of_issue__gte=datetime.datetime.strptime(date_of_issue_param, '%Y-%m-%d').date()).filter(
            date_of_expiry__lte=datetime.datetime.strptime(date_of_expiry_param, '%Y-%m-%d').date())
    elif date_of_issue_param != '':
        results = results.filter(date_of_issue__gte=datetime.datetime.strptime(date_of_issue_param, '%Y-%m-%d').date())
    elif date_of_expiry_param != '':
        results = results.filter(
            date_of_expiry__lte=datetime.datetime.strptime(date_of_expiry_param, '%Y-%m-%d').date())

    if identification_no_param != '':
        results = results.filter(identification_number=identification_no_param)

    if name_param != '':
        results = results.filter(first_name__contains=name_param)

    if last_name_param != '':
        results = results.filter(last_name__contains=last_name_param)
    return results
