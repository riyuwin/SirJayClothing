from django.shortcuts import render
from rest_framework.authtoken.models import Token 

from django.http import JsonResponse
import requests
 
     
#@login_required
def LaunchIndex(request):
    user_id = request.user.id if request.user.is_authenticated else None
    username = request.user.username if request.user.is_authenticated else None
    user_token = None
    if request.user.is_authenticated:
        try:
            user_token = Token.objects.get(user=request.user)
        except Token.DoesNotExist:
            # Handle the case where the token doesn't exist for the user
            pass
    
    return render(request, "index.html", {'logged_in': request.user.is_authenticated, 'user_id': user_id, 'username': username, 'user_token': user_token})
 

def LaunchAppointmentForm(request):  
    services_api_url = request.build_absolute_uri('/api/inventory/services/')
 
    services_response = requests.get(services_api_url)

    # Check if the request was successful (status code 200)
    if services_response.status_code == 200:
        # Parse the JSON response
        services_data = services_response.json() 

        #result = my_task.delay(3, 5)

        # Pass the data to the template for rendering
        #return render(request, 'AppointmentForm.html')
        return render(request, 'AppointmentForm.html', {'services': services_data})
    else:
        # Handle the case when the API request fails (e.g., return an error message)
        return render(request, 'error_template.html', {'message': 'Failed to fetch data from API'}) 
 


def SuccessPage(request):
    return render(request, 'Success.html')


def AccountInformationPage(request):
    customer_api_url = request.build_absolute_uri('/api/customer/')
 
    customer_response = requests.get(customer_api_url)

    user = request.user

    # Check if the user is authenticated
    if user.is_authenticated:
 
        # Get or create token for the user
        token, _ = Token.objects.get_or_create(user=user)


        # Check if the request was successful (status code 200)
        if customer_response.status_code == 200:
            # Parse the JSON response
            customer_data = customer_response.json() 
    
            #return render(request, 'AppointmentForm.html')
            return render(request, 'account_information.html', {'customers': customer_data, 'account_token': token})
        else:
            # Handle the case when the API request fails (e.g., return an error message)
            return render(request, 'error_template.html', {'message': 'Failed to fetch data from API'}) 

def ScheduledAppointmentPage(request):
    customer_api_url = request.build_absolute_uri('/api/customer/')
    appointment_details_api_url = request.build_absolute_uri('/api/appointment/appointment_details')
 
    customer_response = requests.get(customer_api_url)
    appointment_details_response = requests.get(appointment_details_api_url)

    user = request.user

    # Check if the user is authenticated
    if user.is_authenticated:
 
        # Get or create token for the user
        token, _ = Token.objects.get_or_create(user=user)


        # Check if the request was successful (status code 200)
        if appointment_details_response.status_code == 200:
            # Parse the JSON response
            customer_data = customer_response.json() 
            appointment_data = appointment_details_response.json() 
    
            #return render(request, 'AppointmentForm.html')
            return render(request, 'scheduled_appointment.html', {'customers': customer_data, 'account_token': token, 'appointment_details': appointment_data})
        else:
            # Handle the case when the API request fails (e.g., return an error message)
            return render(request, 'error_template.html', {'message': 'Failed to fetch data from API'}) 


def CustomerAppointmentPage(request):
    customer_api_url = request.build_absolute_uri('/api/customer/')
    appointment_details_api_url = request.build_absolute_uri('/api/appointment/appointment_details')
    services_api_url = request.build_absolute_uri('/api/inventory/services')
 
    customer_response = requests.get(customer_api_url)
    appointment_details_response = requests.get(appointment_details_api_url)
    services_details_response = requests.get(services_api_url)

    user = request.user

    # Check if the user is authenticated
    if user.is_authenticated:
        url_id = request.GET.get('id')

        if not url_id:
            return JsonResponse({'error': 'ID parameter is missing.'}, status=400)

        # Get or create token for the user
        token, _ = Token.objects.get_or_create(user=user)


        # Check if the request was successful (status code 200)
        if appointment_details_response.status_code == 200:
            # Parse the JSON response
            customer_data = customer_response.json() 
            appointment_data = appointment_details_response.json() 
            services_data = services_details_response.json() 
    
            #return render(request, 'AppointmentForm.html')
            return render(request, 'customer_appointment.html', {'customers': customer_data, 'account_token': token, 'appointment_details': appointment_data, 'url_id': url_id, 'services': services_data})
        else:
            # Handle the case when the API request fails (e.g., return an error message)
            return render(request, 'error_template.html', {'message': 'Failed to fetch data from API'}) 
