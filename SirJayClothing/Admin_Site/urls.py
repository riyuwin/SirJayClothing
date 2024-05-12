from django.urls import path
from Admin_Site import views

urlpatterns = [
    path('', views.Home, name='Home'),
    path('appointment', views.AppointmentPage, name='Admin_Site'),
    #path('login', views.Login, name='Login'),
]