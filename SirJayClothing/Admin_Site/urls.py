from django.urls import path
from Admin_Site import views

urlpatterns = [
    path('', views.Home, name='Home'),
    #path('appointment/', views.AppointmentPage, name='Admin_Site'),
    path('manage_appointment/', views.ManageAppointmentPage, name='manage_appoinment'),

    path('appointment_details/', views.AppointmentDetailsPage, name='appointment_details'),

]