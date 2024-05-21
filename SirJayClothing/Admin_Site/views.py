from django.shortcuts import render
from django.http import HttpResponse
import requests

from django.shortcuts import render, get_object_or_404
from api.models import Services, Appointment

from django.shortcuts import render, redirect

from rest_framework.authtoken.models import Token 

#from .task import my_task
import time 
from datetime import datetime

def DashboardPage(request):
    user_id = request.user.id if request.user.is_authenticated else None
    username = request.user.username if request.user.is_authenticated else None
    user_token = None

    if request.user.is_authenticated:
        try:
            user_token = Token.objects.get(user=request.user)
        except Token.DoesNotExist:
            pass

    redirect_response = admin_account_checker(request)
    if redirect_response:
        return redirect_response
    
    appointment_api_url = request.build_absolute_uri('/api/appointment/appointment_details/')
    customers_api_url = request.build_absolute_uri('/api/customer/')
    services_api_url = request.build_absolute_uri('/api/inventory/services/')
    appointment_query_api_url = request.build_absolute_uri('/api/appointment/appointment_query/')

    # Make GET requests to the API endpoints
    appointment_response = requests.get(appointment_api_url)
    recent_appointment_response = requests.get(appointment_api_url, params={'recent': 'true'})
    customer_response = requests.get(customers_api_url)
    services_response = requests.get(services_api_url)
    appointment_query_response = requests.get(appointment_query_api_url)

    # Calculate the total number of pending appointments
    total_pending_appointments = Appointment.objects.filter(appointmentStatus="Pending").count()
    total_accepted_appointments = Appointment.objects.filter(appointmentStatus="Accepted").count()

    # Check if the requests were successful (status code 200)
    if all(response.status_code == 200 for response in [appointment_response, recent_appointment_response, customer_response, services_response]):
        # Parse the JSON responses
        appointment_data = appointment_response.json()
        recent_appointment_data = recent_appointment_response.json()
        customer_data = customer_response.json()
        services_data = services_response.json()
        appointment_query_data = appointment_query_response.json()

        appointment_query_queries = sorted(appointment_query_data, key=lambda x: x['date_added'], reverse=True)[:5]
        recent_appointment_queries = sorted(recent_appointment_data, key=lambda x: x['appointmentDate'], reverse=True)[:5]

        # Filter the data to include only "Pending" appointments
        pending_appointments = [entry for entry in recent_appointment_data ] 
        # Count the unique customers
        total_unique_customers = len(pending_appointments)

        # Pass the data to the template for rendering
        return render(request, 'dashboard.html', 
                        {'total_pending_appointments': total_pending_appointments, 
                         'total_accepted_appointments': total_accepted_appointments, 
                        'appointments': appointment_data,  
                        'customers': customer_data, 
                        'services': services_data,
                        'recent_appointments': recent_appointment_queries,  
                        'total_pending_customer': total_unique_customers,
                        'appointment_query': appointment_query_queries,
                        'logged_in': request.user.is_authenticated, 
                        'user_id': user_id, 
                        'username': username, 
                        'user_token': user_token})
    else:
        return render(request, 'error_template.html', {'message': 'Failed to fetch data from API'})

def ManageAppointmentPage(request):
    user_id = request.user.id if request.user.is_authenticated else None
    username = request.user.username if request.user.is_authenticated else None
    user_token = None

    if request.user.is_authenticated:
        try:
            user_token = Token.objects.get(user=request.user)
        except Token.DoesNotExist:
            pass

    redirect_response = admin_account_checker(request)
    if redirect_response:
        return redirect_response

    appointment_api_url = request.build_absolute_uri('/api/appointment/appointment_details/')
    customers_api_url = request.build_absolute_uri('/api/customer/')

    # Fetch all appointments and recent appointments from the API
    appointment_response = requests.get(appointment_api_url)
    recent_appointment_response = requests.get(appointment_api_url, params={'recent': 'true'})
    customer_response = requests.get(customers_api_url)

    if appointment_response.status_code == 200 and recent_appointment_response.status_code == 200:
        appointment_data = appointment_response.json()
        recent_appointment_data = recent_appointment_response.json()
        customer_data = customer_response.json()

        return render(request, 'appointment.html', {
            'appointments': appointment_data,
            'recent_appointments': recent_appointment_data,  
            'customers': customer_data,
            'logged_in': request.user.is_authenticated,
            'user_id': user_id,
            'username': username,
            'user_token': user_token
        })
    else:
        return render(request, 'error_template.html', {'message': 'Failed to fetch data from API'})

def AppointmentDetailsPage(request): 
    user_id = request.user.id if request.user.is_authenticated else None
    username = request.user.username if request.user.is_authenticated else None
    user_token = None

    if request.user.is_authenticated:
        try:
            user_token = Token.objects.get(user=request.user)
        except Token.DoesNotExist:
            # Handle the case where the token doesn't exist for the user
            pass
     
    redirect_response = admin_account_checker(request)
    if redirect_response:
        return redirect_response
     
    appointment_api_url = request.build_absolute_uri('/api/appointment/appointment_details/')
    customers_api_url = request.build_absolute_uri('/api/customer/')
    necessaryitems_api_url = request.build_absolute_uri('/api/inventory/necessaryitems/')
    product_api_url = request.build_absolute_uri('/api/inventory/product/')
    appointmentquery_api_url = request.build_absolute_uri('/api/appointment/appointment_query')
    services_api_url = request.build_absolute_uri('/api/inventory/services/')  

    # Make a GET request to the API endpoint
    appointment_response = requests.get(appointment_api_url)
    customer_response = requests.get(customers_api_url)
    necessaryitems_response = requests.get(necessaryitems_api_url)
    product_response = requests.get(product_api_url)
    appointmentquery_response = requests.get(appointmentquery_api_url)
    services_response = requests.get(services_api_url)

    # get url parse
    id_value = request.GET.get('id')

    # Check if the request was successful (status code 200)
    if appointment_response.status_code == 200:
        # Parse the JSON response
        appointment_data = appointment_response.json()
        customer_data = customer_response.json()
        necessaryitems_data = necessaryitems_response.json()
        product_data = product_response.json()
        appointmentquery_data = appointmentquery_response.json()
        services_data = services_response.json()

        #result = my_task.delay(3, 5)

        # Pass the data to the template for rendering
        return render(request, 'appointment_details.html', {'appointments': appointment_data, 'customers': customer_data, 'necessaryitems': necessaryitems_data, 'products': product_data, 'appointmentquery': appointmentquery_data, 'id_value': id_value, 'logged_in': request.user.is_authenticated, 'user_id': user_id, 'username': username, 'user_token': user_token, 'services': services_data})
    else: 
        return render(request, 'error_template.html', {'message': 'Failed to fetch data from API'}) 


def ProductCategoriesPage(request): 
    user_id = request.user.id if request.user.is_authenticated else None
    username = request.user.username if request.user.is_authenticated else None
    user_token = None

    if request.user.is_authenticated:
        try:
            user_token = Token.objects.get(user=request.user)
        except Token.DoesNotExist: 
            pass
     
    redirect_response = admin_account_checker(request)
    if redirect_response:
        return redirect_response
     
    appointment_api_url = request.build_absolute_uri('/api/appointment/appointment_details/')
    customers_api_url = request.build_absolute_uri('/api/customer/')
    necessaryitems_api_url = request.build_absolute_uri('/api/inventory/necessaryitems/')
    category_api_url = request.build_absolute_uri('/api/inventory/category/')

    # Make a GET request to the API endpoint
    appointment_response = requests.get(appointment_api_url)
    customer_response = requests.get(customers_api_url)
    necessaryitems_response = requests.get(necessaryitems_api_url)
    category_response = requests.get(category_api_url)

    # get url parse
    id_value = request.GET.get('id')

    # Check if the request was successful (status code 200)
    if appointment_response.status_code == 200:
        # Parse the JSON response
        appointment_data = appointment_response.json()
        customer_data = customer_response.json()
        necessaryitems_data = necessaryitems_response.json()
        category_data = category_response.json()

        #result = my_task.delay(3, 5)

        # Pass the data to the template for rendering
        return render(request, 'supply_type.html', {'appointments': appointment_data, 'customers': customer_data, 'necessaryitems': necessaryitems_data, 'categories': category_data, 'logged_in': request.user.is_authenticated, 'user_id': user_id, 'username': username, 'user_token': user_token})
    else: 
        return render(request, 'error_template.html', {'message': 'Failed to fetch data from API'}) 


def SupplierPage(request): 
    user_id = request.user.id if request.user.is_authenticated else None
    username = request.user.username if request.user.is_authenticated else None
    user_token = None

    if request.user.is_authenticated:
        try:
            user_token = Token.objects.get(user=request.user)
        except Token.DoesNotExist: 
            pass

    redirect_response = admin_account_checker(request)
    if redirect_response:
        return redirect_response
      
    supplier_api_url = request.build_absolute_uri('/api/inventory/supplier/') 

    # Make a GET request to the API endpoint
    supplier_response = requests.get(supplier_api_url) 
 

    # Check if the request was successful (status code 200)
    if supplier_response.status_code == 200:
        # Parse the JSON response
        supplier_data = supplier_response.json() 

        #result = my_task.delay(3, 5)

        # Pass the data to the template for rendering
        return render(request, 'suppliers.html', {'suppliers': supplier_data, 'logged_in': request.user.is_authenticated, 'user_id': user_id, 'username': username, 'user_token': user_token})
    else:
        # Handle the case when the API request fails (e.g., return an error message)
        return render(request, 'error_template.html', {'message': 'Failed to fetch data from API'}) 

def InventoryPage(request): 
    user_id = request.user.id if request.user.is_authenticated else None
    username = request.user.username if request.user.is_authenticated else None
    user_token = None

    if request.user.is_authenticated:
        try:
            user_token = Token.objects.get(user=request.user)
        except Token.DoesNotExist:
            # Handle the case where the token doesn't exist for the user
            pass

    redirect_response = admin_account_checker(request)
    if redirect_response:
        return redirect_response
    
     # Assuming your API endpoint is '/api/endpoint/' (replace with your actual endpoint)
    product_api_url = request.build_absolute_uri('/api/inventory/product/') 
    supplier_api_url = request.build_absolute_uri('/api/inventory/supplier/')
    category_api_url = request.build_absolute_uri('/api/inventory/category/') 

    # Make a GET request to the API endpoint
    product_response = requests.get(product_api_url) 
    supplier_response = requests.get(supplier_api_url) 
    category_response = requests.get(category_api_url) 
 

    # Check if the request was successful (status code 200)
    if supplier_response.status_code == 200:
        # Parse the JSON response
        product_data = product_response.json() 
        supplier_data = supplier_response.json() 
        category_data = category_response.json() 

        #result = my_task.delay(3, 5)

        # Pass the data to the template for rendering
        return render(request, 'inventory.html', {'suppliers': supplier_data, 'products': product_data, 'categories': category_data, 'logged_in': request.user.is_authenticated, 'user_id': user_id, 'username': username, 'user_token': user_token})
    else:
        # Handle the case when the API request fails (e.g., return an error message)
        return render(request, 'error_template.html', {'message': 'Failed to fetch data from API'}) 


def CustomerPage(request): 
    user_id = request.user.id if request.user.is_authenticated else None
    username = request.user.username if request.user.is_authenticated else None
    user_token = None

    if request.user.is_authenticated:
        try:
            user_token = Token.objects.get(user=request.user)
        except Token.DoesNotExist:
            # Handle the case where the token doesn't exist for the user
            pass
     

    redirect_response = admin_account_checker(request)
    if redirect_response:
        return redirect_response
     
    customer_api_url = request.build_absolute_uri('/api/customer/')   

    # Make a GET request to the API endpoint
    customer_response = requests.get(customer_api_url)  
 

    # Check if the request was successful (status code 200)
    if customer_response.status_code == 200:
        # Parse the JSON response
        customer_data = customer_response.json()  

        #result = my_task.delay(3, 5)

        # Pass the data to the template for rendering
        return render(request, 'customer.html', { 'customers': customer_data, 'logged_in': request.user.is_authenticated, 'user_id': user_id, 'username': username, 'user_token': user_token})
    else: 
        return render(request, 'error_template.html', {'message': 'Failed to fetch data from API'}) 


def CustomerDetailsPage(request):
    user_id = request.user.id if request.user.is_authenticated else None
    username = request.user.username if request.user.is_authenticated else None
    user_token = None

    if request.user.is_authenticated:
        try:
            user_token = Token.objects.get(user=request.user)
        except Token.DoesNotExist:
            # Handle the case where the token doesn't exist for the user
            pass

    redirect_response = admin_account_checker(request)
    if redirect_response:
        return redirect_response  
    
    customer_api_url = request.build_absolute_uri('/api/customer/')   
    appointment_api_url = request.build_absolute_uri('/api/appointment/appointment_details/')   
    services_api_url = request.build_absolute_uri('/api/inventory/services/')  

    # Make a GET request to the API endpoint
    customer_response = requests.get(customer_api_url)
    appointment_response = requests.get(appointment_api_url)  
    services_response = requests.get(services_api_url)     
 

    # Check if the request was successful (status code 200)
    if customer_response.status_code == 200:
        # Parse the JSON response
        customer_data = customer_response.json()  
        appointment_data = appointment_response.json() 
        services_data = services_response.json() 

        #result = my_task.delay(3, 5)

        # Pass the data to the template for rendering
        return render(request, 'customer_details.html', { 'customers': customer_data, 
                                                        'appointments': appointment_data, 
                                                        'logged_in': request.user.is_authenticated, 
                                                        'user_id': user_id, 
                                                        'username': username, 
                                                        'user_token': user_token,
                                                        'services': services_data})
    else: 
        return render(request, 'error_template.html', {'message': 'Failed to fetch data from API'}) 


def ServicesPage(request):
    user_id = request.user.id if request.user.is_authenticated else None
    username = request.user.username if request.user.is_authenticated else None
    user_token = None

    if request.user.is_authenticated:
        try:
            user_token = Token.objects.get(user=request.user)
        except Token.DoesNotExist:
            # Handle the case where the token doesn't exist for the user
            pass
    redirect_response = admin_account_checker(request)
    if redirect_response:
        return redirect_response
     
    product_api_url = request.build_absolute_uri('/api/inventory/product/')
    supplier_api_url = request.build_absolute_uri('/api/inventory/supplier/')
    category_api_url = request.build_absolute_uri('/api/inventory/category/')
    services_api_url = request.build_absolute_uri('/api/inventory/services/')
 
    product_response = requests.get(product_api_url)
    supplier_response = requests.get(supplier_api_url)
    category_response = requests.get(category_api_url)
    services_response = requests.get(services_api_url)

    # Check if the request was successful (status code 200)
    if all(response.status_code == 200 for response in [product_response, supplier_response, category_response, services_response]):
        # Parse the JSON responses
        product_data = product_response.json()
        supplier_data = supplier_response.json()
        category_data = category_response.json()
        services_data = services_response.json()

        # Fetch all services from the database
        db_services = Services.objects.all()

        # Pass the data to the template for rendering
        context = {
            'products': product_data,
            'suppliers': supplier_data,
            'categories': category_data, 
            'services': db_services,
            'logged_in': request.user.is_authenticated, 
            'user_id': user_id, 
            'username': username, 
            'user_token': user_token
        }
        return render(request, 'services.html', context)
    else: 
        return render(request, 'error_template.html', {'message': 'Failed to fetch data from API'})
    
def admin_account_checker(request): 
    user = request.user

    if user.is_authenticated: 
        user_type = 'Admin' if user.is_staff or user.is_superuser else 'Customer'
        
        if user_type != "Admin":
            print(user_type)
            return redirect('/api/authorized_template/')
    return None   



def customer_account_checker(request): 
    user = request.user

    if user.is_authenticated:
        # Determine if the user is admin or customer
        user_type = 'Admin' if user.is_staff or user.is_superuser else 'Customer'

        if user_type != "Customer":
            return redirect('/authorized_template/')
    return None  # Return None if the user is an admin or if the user is not authenticated