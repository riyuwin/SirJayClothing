from django.urls import path
from Client_Site import views

urlpatterns = [
    # Notifier
    path('success_page/', views.SuccessPage, name='success_page'),
 
    # Client Interface
    path('appointment_information/', views.ScheduledAppointmentPage, name='appointment_information'),
    path('account_information/', views.AccountInformationPage, name='account_information'),
    path('customer_information/', views.CustomerAppointmentPage, name='customer_information'),

    # NavBar Interface
    path('guest_appointment_form/', views.LaunchAppointmentForm, name='guest_appointment_form'),
    path('guest_services/', views.ServicesPage, name='guest_appointment_form'),
    path('guest_services_details/', views.ServicesDetailsPage, name='guest_services_details'),
    path('guest_contact/', views.LaunchContact, name='guest_contact'),
    path('', views.LaunchIndex, name='index'),
]