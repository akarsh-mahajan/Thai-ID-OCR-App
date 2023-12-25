# Thai ID OCR App

## Introduction

The Thai ID OCR App is a powerful and efficient application designed to extract information from Thai identification cards using Optical Character Recognition (OCR) technology.
This application streamlines the process of capturing and interpreting critical details like name, last name, date of birth, date of issue, date of expiry from Thai ID cards,
providing a reliable and accurate solution for data extraction.

## Web App Link and Demo
This project is currently hosted on: http://akarsh23.pythonanywhere.com/

Link to demo: https://github.com/akarsh-mahajan/Thai-ID-OCR-App/assets/108885564/1331b41f-0d18-48ec-ad56-b5071ddf9e4b

## Description




Web App provides the functionality to upload a Thai ID Card and view its OCR result, view the previous OCR operations, filter the records in the database through various parameters like name, last name, date of birth,
date of issue, date of expiry and fetching and deleting an existing record by Thai identification number.

In this project I have used [google-cloud-vision-api](https://cloud.google.com/vision/docs/ocr#optical_character_recognition_ocr) for performing OCR and extracting text from images and
then used the custom logic to extract the necessary details from cloud vision API response.
I have used an inbuilt django housed sqlite3 database for our application (keeping in mind that this is a small scale Web App).

### The sequence diagram to show interactions between objects
![Sequence Diagram](https://github.com/akarsh-mahajan/Thai-ID-OCR-App/assets/108885564/78eae24d-04ea-4c77-af25-f3ec086a7d6e)


## How to Run Locally

To Run the project in your local system, 
1. First, ensure you have a suitable Python version (I have used Python 3.10 here).
2. Next, create a virtual environment in your local system and install dependencies from requirements.txt using **'pip install -r requirements. txt'**
3. Now paste your google-cloud-vision-api JSON file in the project directory and mention it in the settings.py of your Django Project.
4. Run **"python manage.py makemigrations"** then **"python manage.py migrate"** to create and setup the database.
5. Now, Run **"python manage.py runserver"** to run the project.

