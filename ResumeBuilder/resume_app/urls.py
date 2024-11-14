# resume_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Root URL mapped to home view
    path('signup/', views.signup, name='signup'),  # Add this line
    path('upload/', views.upload_certificate, name='upload_certificate'),
    path('certificates/', views.certificate_list, name='certificate_list'),
    path('generate_resume/', views.generate_resume, name='generate_resume'),
    path('profile/', views.profile, name='profile'),  # Add this line for profile view
]
