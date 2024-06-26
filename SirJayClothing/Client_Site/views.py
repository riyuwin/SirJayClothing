from django.shortcuts import render
from rest_framework.authtoken.models import Token 

from django.http import JsonResponse
import requests

from api.models import Services, Customer

from django.shortcuts import render, redirect
 
     
#@login_required
def LaunchIndex(request): 
    user_id = request.user.id if request.user.is_authenticated else None
    username = request.user.username if request.user.is_authenticated else None
    user_token = None 

    user = request.user

    if request.user.is_authenticated:
        try:
            user_token = Token.objects.get(user=request.user)
        except Token.DoesNotExist:
            # Handle the case where the token doesn't exist for the user
            pass
    
    user_type = 'Admin' if user.is_staff or user.is_superuser else 'Customer'
    return render(request, "index.html", {'logged_in': request.user.is_authenticated, 'user_id': user_id, 'username': username, 'user_token': user_token, 'user_type': user_type})
 
def ServicesPage(request):  
    customer_api_url = request.build_absolute_uri('/api/customer/')
    appointment_details_api_url = request.build_absolute_uri('/api/appointment/appointment_details')
    services_api_url = request.build_absolute_uri('/api/inventory/services')
 
    customer_response = requests.get(customer_api_url)
    appointment_details_response = requests.get(appointment_details_api_url)
    services_details_response = requests.get(services_api_url)

    user = request.user
    
    user_id = request.user.id if request.user.is_authenticated else None
    username = request.user.username if request.user.is_authenticated else None
 

    # Fetch all services from the database
    db_services = Services.objects.all()

    # Check if the request was successful (status code 200)
    if appointment_details_response.status_code == 200:
        # Parse the JSON response
        customer_data = customer_response.json() 
        appointment_data = appointment_details_response.json() 
        services_data = services_details_response.json() 

        return render(request, 'guest_services.html', {'logged_in': user.is_authenticated, 'customers': customer_data, 'appointment_details': appointment_data, 'services': db_services, 'user_id': user_id, 'username': username})
    else:
        # Handle the case when the API request fails (e.g., return an error message)
        return render(request, 'error_template.html', {'message': 'Failed to fetch data from API'})  
    
#@login_required
def LaunchAboutPage(request): 
    user_id = request.user.id if request.user.is_authenticated else None
    username = request.user.username if request.user.is_authenticated else None
    user_token = None 

    user = request.user

    if request.user.is_authenticated:
        try:
            user_token = Token.objects.get(user=request.user)
        except Token.DoesNotExist:
            # Handle the case where the token doesn't exist for the user
            pass
    
    user_type = 'Admin' if user.is_staff or user.is_superuser else 'Customer'
    return render(request, "guest_about.html", {'logged_in': request.user.is_authenticated, 'user_id': user_id, 'username': username, 'user_token': user_token, 'user_type': user_type})
 


#@login_required
def LaunchContact(request): 
    user_id = request.user.id if request.user.is_authenticated else None
    username = request.user.username if request.user.is_authenticated else None
    user_token = None 

    user = request.user

    if request.user.is_authenticated:
        try:
            user_token = Token.objects.get(user=request.user)
        except Token.DoesNotExist:
            # Handle the case where the token doesn't exist for the user
            pass
    
    user_type = 'Admin' if user.is_staff or user.is_superuser else 'Customer'
    return render(request, "guest_contact.html", {'logged_in': request.user.is_authenticated, 'user_id': user_id, 'username': username, 'user_token': user_token, 'user_type': user_type})
 

def LaunchAppointmentForm(request):  
    
    redirect_response = customer_account_checker(request)
    if redirect_response:
        return redirect_response
    

    services_api_url = request.build_absolute_uri('/api/inventory/services/')
 
    services_response = requests.get(services_api_url)

    # Check if the request was successful (status code 200)
    if services_response.status_code == 200:
        # Parse the JSON response
        services_data = services_response.json() 

        #result = my_task.delay(3, 5)

        # Pass the data to the template for rendering
        #return render(request, 'AppointmentForm.html')
        return render(request, 'guest_appointment_form.html', {'services': services_data})
    else:
        # Handle the case when the API request fails (e.g., return an error message)
        return render(request, 'error_template.html', {'message': 'Failed to fetch data from API'}) 

def SuccessPage(request):
    return render(request, 'Success.html')

def AccountInformationPage(request):
    
    redirect_response = customer_account_checker(request)
    if redirect_response:
        return redirect_response
    
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
    redirect_response = customer_account_checker(request)
    if redirect_response:
        return redirect_response
    
    customer_api_url = request.build_absolute_uri('/api/customer/')
    appointment_details_api_url = request.build_absolute_uri('/api/appointment/appointment_details')
    services_api_url = request.build_absolute_uri('/api/inventory/services')
 
    customer_response = requests.get(customer_api_url)
    appointment_details_response = requests.get(appointment_details_api_url)
    services_response = requests.get(services_api_url)

    # Fetch all services from the database
    db_services = Services.objects.all()

    user = request.user

    # Check if the user is authenticated
    if user.is_authenticated:
 
        # Get or create token for the user
        token, _ = Token.objects.get_or_create(user=user)

        obj_to_customer_id = Customer.objects.get(accountToken=token)  # Replace obj_id with the ID of the object you want to delete
        

        # Check if the request was successful (status code 200)
        if appointment_details_response.status_code == 200:
            # Parse the JSON response
            customer_data = customer_response.json() 
            appointment_data = appointment_details_response.json() 
            services_data = services_response.json() 
    
            #return render(request, 'AppointmentForm.html')
            return render(request, 'scheduled_appointment.html', {'customers': customer_data, 'customerid': obj_to_customer_id.id, 'account_token': token, 'appointment_details': appointment_data, 'services': db_services})
        else:
            # Handle the case when the API request fails (e.g., return an error message)
            return render(request, 'error_template.html', {'message': 'Failed to fetch data from API'}) 


def CustomerAppointmentPage(request):
    
    redirect_response = customer_account_checker(request)
    if redirect_response:
        return redirect_response
    
    customer_api_url = request.build_absolute_uri('/api/customer/')
    appointment_details_api_url = request.build_absolute_uri('/api/appointment/appointment_details')
    services_api_url = request.build_absolute_uri('/api/inventory/services')
    appointmentquery_api_url = request.build_absolute_uri('/api/appointment/appointment_query')
 
    customer_response = requests.get(customer_api_url)
    appointment_details_response = requests.get(appointment_details_api_url)
    services_details_response = requests.get(services_api_url)
    appointmentquery_response = requests.get(appointmentquery_api_url)

    # Fetch all services from the database
    db_services = Services.objects.all()  

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
            appointmentquery_data = appointmentquery_response.json() 
    
            #return render(request, 'AppointmentForm.html')
            return render(request, 'appointment_information.html', {'customers': customer_data, 'account_token': token, 'appointment_details': appointment_data, 'url_id': url_id, 'services': db_services, 'appointmentquery': appointmentquery_data})
        else:
            # Handle the case when the API request fails (e.g., return an error message)
            return render(request, 'error_template.html', {'message': 'Failed to fetch data from API'}) 

def ServicesDetailsPage(request):
    customer_api_url = request.build_absolute_uri('/api/customer/')
    appointment_details_api_url = request.build_absolute_uri('/api/appointment/appointment_details')
    services_api_url = request.build_absolute_uri('/api/inventory/services')

    user = request.user

    user_id = user.id if user.is_authenticated else None
    username = user.username if user.is_authenticated else None
    token = None

    if user.is_authenticated:
        # Get or create token for the user
        token, _ = Token.objects.get_or_create(user=user)

    # Fetch all services from the database
    db_services = Services.objects.all()
    url_id = request.GET.get('id')

    # Initialize data containers
    customer_data = None
    appointment_data = None
    services_data = None

    # Check if all requests are successful (status code 200)
    try:
        customer_response = requests.get(customer_api_url)
        customer_response.raise_for_status()
        customer_data = customer_response.json()

        appointment_details_response = requests.get(appointment_details_api_url)
        appointment_details_response.raise_for_status()
        appointment_data = appointment_details_response.json()

        services_details_response = requests.get(services_api_url)
        services_details_response.raise_for_status()
        services_data = services_details_response.json()

    except requests.exceptions.RequestException as e:
        # Handle the case when the API request fails (e.g., return an error message)
        return render(request, 'error_template.html', {'message': f'Failed to fetch data from API: {e}'})

    return render(request, 'guest_services_details.html', {
        'logged_in': user.is_authenticated,
        'url_id': url_id,
        'services': db_services,
        'user_id': user_id,
        'username': username,
        'customer_data': customer_data,
        'appointment_data': appointment_data,
        'services_data': services_data,
    })


def admin_account_checker(request): 
    user = request.user

    if user.is_authenticated:
        # Determine if the user is admin or customer
        user_type = 'Admin' if user.is_staff or user.is_superuser else 'Customer'
        
        if user_type == "Customer":
            print(user_type)
            return redirect('/api/authorized_template/')
    return None  # Return None if the user is an admin or if the user is not authenticated


def customer_account_checker(request): 
    user = request.user

    if user.is_authenticated:
        # Determine if the user is admin or customer
        user_type = 'Admin' if user.is_staff or user.is_superuser else 'Customer'

        if user_type != "Customer":
            return redirect('/api/authorized_template/')
    else:
        return redirect('/account/login_page/')
    return None  # Return None if the user is an admin or if the user is not authenticated
