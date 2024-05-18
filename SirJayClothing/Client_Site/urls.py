from django.urls import path
from Client_Site import views

urlpatterns = [
    # Notifier
    path('success_page/', views.SuccessPage, name='success_page'),
 
    # Client Interface
    path('account_information/', views.AccountInformationPage, name='account_information'),
    path('scheduled_information/', views.ScheduledAppointmentPage, name='scheduled_information'),
    path('customer_information/', views.CustomerAppointmentPage, name='customer_information'),
    path('appointment_form/', views.LaunchAppointmentForm, name='appointment_form'),
    path('', views.LaunchIndex, name='index'),
]