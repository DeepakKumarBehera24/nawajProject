import os
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
import re


def extract_text_from_pdf(file_path):
    text = ""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # First, try extracting text using pdfplumber (for text-based PDFs)
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()

    # If the text extraction is empty or not sufficient, fall back to OCR
    if not text.strip():
        print("Text extraction failed, attempting OCR...")
        images = convert_from_path(file_path)
        for image in images:
            text += pytesseract.image_to_string(image)
        if not text.strip():
            raise Exception("OCR failed to extract any text from the PDF.")

    # Print extracted text for debugging purposes
    print("Raw Extracted Text:\n", text)
    return text


def extract_information(text):
    # Regex patterns for different fields
    certificate_url_pattern = r"Certificate url:\s*(https?://[\S]+)"
    course_name_pattern = r"CERTIFICATE OF COMPLETION\s+([\s\S]+?)\s+Instructors"
    instructors_pattern = r"Instructors\s+([\s\S]+?)\s+Date"
    date_pattern = r"Date\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})"

    # Match patterns and extract data
    certificate_url_match = re.search(certificate_url_pattern, text)
    course_name_match = re.search(course_name_pattern, text)
    instructors_match = re.search(instructors_pattern, text)
    date_match = re.search(date_pattern, text)

    certificate_url = certificate_url_match.group(1) if certificate_url_match else 'Not Found'
    course_name = course_name_match.group(1) if course_name_match else 'Not Found'
    instructors = instructors_match.group(1) if instructors_match else 'Not Found'
    date = date_match.group(1) if date_match else 'Not Found'

    # Extract email, phone, and skills (if needed)
    email = None  # Assuming you don't have emails in the certificate
    phone = None  # Assuming you don't have phone numbers in the certificate
    skills = []  # Assuming no specific skills are listed in the certificate

    # Return the extracted information
    return {
        'certificate_url': certificate_url,
        'course_name': course_name,
        'instructors': instructors,
        'date': date,
        'email': email,
        'phone': phone,
        'skills': skills
    }

