from django.urls import path
from Client_Site import views

urlpatterns = [
    path('add_customer/', views.LaunchAddCustomer, name='CustomerPage'),
    path('', views.LaunchIndex, name='index'),
]