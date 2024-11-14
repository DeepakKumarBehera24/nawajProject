from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import CertificateUploadForm
from .models import Certificate
import pytesseract
import pdfplumber
import spacy

from .utils import extract_text_from_pdf, extract_information

# Load NLP model
nlp = spacy.load('en_core_web_sm')


def home(request):
    return render(request, 'resume_app/home.html')


@login_required
def upload_certificate(request):
    if request.method == 'POST':
        form = CertificateUploadForm(request.POST, request.FILES)
        if form.is_valid():
            certificate = form.save(commit=False)
            certificate.user = request.user  # Ensure the logged-in user is assigned to the certificate
            certificate.save()
            return redirect('certificate_list')  # Redirect to certificate list or any other page
    else:
        form = CertificateUploadForm()
    return render(request, 'resume_app/upload_certificate.html', {'form': form})


def certificate_list(request):
    certificates = Certificate.objects.filter(user=request.user)
    return render(request, 'resume_app/certificate_list.html', {'certificates': certificates})


@login_required
def generate_resume(request):
    if request.method == 'POST':
        # Ensure the user has uploaded a certificate
        certificate = Certificate.objects.filter(user=request.user).last()
        if not certificate:
            # Redirect or show an error if no certificate is uploaded
            return redirect('upload_certificate')  # Redirect to upload page if no certificate exists

        # Extract text from the uploaded certificate PDF
        text = extract_text_from_pdf(certificate.certificate_file.path)

        # Extract information from the text
        extracted_info = extract_information(text)

        # Pass extracted information to the template
        context = {
            'des': text,
            'certificate': certificate,
            'institution': extracted_info.get('institution', 'Not Found'),
            'date': extracted_info.get('date', 'Not Found'),
            'email': extracted_info.get('email', 'Not Found'),
            'phone': extracted_info.get('phone', 'Not Found'),
            'skills': extracted_info.get('skills', []),
        }

        return render(request, 'resume_app/generated_resume.html', context)

    return render(request, 'resume_app/upload_certificate.html')


def extract_text_from_certificate(certificate):
    # Open the certificate file and extract text using OCR
    if certificate.certificate_file.name.endswith('.pdf'):
        with pdfplumber.open(certificate.certificate_file) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text()
            return text
    else:
        # Use OCR for image files
        text = pytesseract.image_to_string(certificate.certificate_file.path)
        return text


def extract_course_name(doc):
    # You can improve this to specifically extract the course name
    for ent in doc.ents:
        if ent.label_ == 'ORG':  # Course might be treated as a proper noun or organization
            return ent.text
    return "Not Found"


def extract_institution_name(doc):
    # You can improve this to specifically extract the institution name
    for ent in doc.ents:
        if ent.label_ == 'ORG':  # Likely the institution is identified as an organization
            return ent.text
    return "Not Found"


def extract_date(doc):
    # Extract date (if any)
    for ent in doc.ents:
        if ent.label_ == 'DATE':
            return ent.text
    return "Not Found"


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # After successful signup, redirect to login page
    else:
        form = UserCreationForm()
    return render(request, 'resume_app/signup.html', {'form': form})


@login_required
def profile(request):
    return redirect('upload_certificate')  # Redirect to your desired page after login
