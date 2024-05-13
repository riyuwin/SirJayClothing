# accounts/urls.py

from django.urls import path
from .views import launchIndexPage, loginPage, registerPage

urlpatterns = [ 
    path('', launchIndexPage, name='check_user'),
    path('login_page/', loginPage, name='login_page'),
    path('register_page/', registerPage, name='register_page'),
]