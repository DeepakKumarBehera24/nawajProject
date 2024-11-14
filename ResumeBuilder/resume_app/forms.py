# resume_app/forms.py
from django import forms
from .models import Certificate


class CertificateUploadForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['certificate_file']
