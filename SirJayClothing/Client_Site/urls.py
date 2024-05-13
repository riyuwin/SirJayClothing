from django.urls import path
from Client_Site import views

urlpatterns = [
    # Notifier
    path('success_page/', views.SuccessPage, name='success_page'),
 
    # Client Interface
    path('appointment_form/', views.LaunchAppointmentForm, name='appointment_form'),
    path('', views.LaunchIndex, name='index'),
]