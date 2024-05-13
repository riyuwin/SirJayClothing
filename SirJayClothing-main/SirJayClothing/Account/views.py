from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token 
  
#@login_required
def launchIndexPage(request):
    user_id = request.user.id if request.user.is_authenticated else None
    username = request.user.username if request.user.is_authenticated else None
    user_token = None
    if request.user.is_authenticated:
        try:
            user_token = Token.objects.get(user=request.user)
        except Token.DoesNotExist:
            # Handle the case where the token doesn't exist for the user
            pass

    return render(request, "login_checker.html", {'logged_in': request.user.is_authenticated, 'user_id': user_id, 'username': username, 'user_token': user_token})

def loginPage(request): 
    return render(request, "login.html" )


def registerPage(request): 
    return render(request, "register.html" )
