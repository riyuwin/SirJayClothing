from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from .models import CustomUser
from .serializers import UserSerializer


from api.models import Customer 

@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        # Extract specific fields from request.data
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        # Validate extracted data (you may want to add more validation)
        if not (username and email and password):
            return Response({'error': 'Username, email, and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a user with the extracted data
        user_data = {
            'username': username,
            'email': email,
            'password': password,
        }
        serializer = UserSerializer(data=user_data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate a token for the user
            token, _ = Token.objects.get_or_create(user=user)

            # Include token in the response data
            response_data = {
                'token': token.key,
                'user': serializer.data
            }

            # Get form data
            fname = request.POST.get('fname')
            mname = request.POST.get('mname')
            lname = request.POST.get('lname')
            gender = request.POST.get('gender')
            phoneNum = request.POST.get('phoneNum')

            # Save customer data to the database
            customer = Customer.objects.create(
                customerFname=fname,
                customerMname=mname,
                customerLname=lname,
                customerGender=gender,
                customerPhone=phoneNum,
                customerEmail=email,
                accountToken=token.key,
            )

            return Response(response_data, status=status.HTTP_201_CREATED)
            #return redirect('/customer_add_customer')  # Replace '/appointment.html' with your desired URL

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = None
        if '@' in username:
            try:
                user = CustomUser.objects.get(email=username)
            except ObjectDoesNotExist:
                pass

        if not user:
            user = authenticate(username=username, password=password)

        if user:
            login(request, user)  # Set the session for the user
            token, _ = Token.objects.get_or_create(user=user)

            # Check if user is superuser or admin
            if user.is_superuser:
                # Redirect to admin dashboard or specific URL for superuser
                return redirect('/admin/')  # Example redirect to admin dashboard
            else:
                # Redirect to index.html with a token query parameter for normal users
                return redirect(f'/?token={token.key}')

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        logout(request)  # Log the user out
        #return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        return redirect(f'/account/login_page/') # Back to home
 
 
