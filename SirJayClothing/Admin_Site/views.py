from django.shortcuts import render
from django.http import HttpResponse
import requests

#from .task import my_task
import time

#from .task import my_task

def AppointmentPage(request):
    # Assuming your API endpoint is '/api/endpoint/' (replace with your actual endpoint)
    appointment_api_url = request.build_absolute_uri('/api/appointment/appointment_details/')
    customer_api_url = request.build_absolute_uri('/api/customer/')
    product_api_url = request.build_absolute_uri('/api/inventory/product/')
    necessaryitems_api_url = request.build_absolute_uri('/api/inventory/necessaryitems/')

    # Make a GET request to the API endpoints
    appointment_response = requests.get(appointment_api_url)
    customer_response = requests.get(customer_api_url)
    product_response = requests.get(product_api_url)
    necessaryitems_response = requests.get(necessaryitems_api_url)

    # Check if the requests were successful (status code 200)
    if appointment_response.status_code == 200 and customer_response.status_code == 200:
        # Parse the JSON responses
        data = appointment_response.json()
        customer_data = customer_response.json()
        product_data = product_response.json()
        necessaryitems_data = necessaryitems_response.json()

        # Pass the data to the template for rendering
        return render(request, 'appointment.html',
                      {'appointment_details': data,
                       'customer': customer_data,
                       'product': product_data,
                       'necessaryitems': necessaryitems_data})
    else:
        # Handle the case when the API requests fail (e.g., return an error message)
        return render(request, 'error_template.html', {'message': 'Failed to fetch data from API'})

def Home(request):    
    # Assuming your API endpoint is '/api/endpoint/' (replace with your actual endpoint)
    api_url = request.build_absolute_uri('/api/customer/')

    # Make a GET request to the API endpoint
    response = requests.get(api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        #result = my_task.delay(3, 5)

        # Pass the data to the template for rendering
        return render(request, 'customer_list.html', {'customer': data})
    else:
        # Handle the case when the API request fails (e.g., return an error message)
        return render(request, 'error_template.html', {'message': 'Failed to fetch data from API'})


def ManageAppointmentPage(request):
    # Assuming your API endpoint is '/api/endpoint/' (replace with your actual endpoint)
    appointment_api_url = request.build_absolute_uri('/api/appointment/appointment_details/')
    customers_api_url = request.build_absolute_uri('/api/customer/')

    # Make a GET request to the API endpoint
    appointment_response = requests.get(appointment_api_url)
    customer_response = requests.get(customers_api_url)

    # Check if the request was successful (status code 200)
    if appointment_response.status_code == 200:
        # Parse the JSON response
        appointment_data = appointment_response.json()
        customer_data = customer_response.json()

        #result = my_task.delay(3, 5)

        # Pass the data to the template for rendering
        return render(request, 'appointment.html', {'appointments': appointment_data, 'customers': customer_data,})
    else:
        # Handle the case when the API request fails (e.g., return an error message)
        return render(request, 'error_template.html', {'message': 'Failed to fetch data from API'}) 
 

def AppointmentDetailsPage(request): 
     # Assuming your API endpoint is '/api/endpoint/' (replace with your actual endpoint)
    appointment_api_url = request.build_absolute_uri('/api/appointment/appointment_details/')
    customers_api_url = request.build_absolute_uri('/api/customer/')
    necessaryitems_api_url = request.build_absolute_uri('/api/inventory/necessaryitems/')
    product_api_url = request.build_absolute_uri('/api/inventory/product/')

    # Make a GET request to the API endpoint
    appointment_response = requests.get(appointment_api_url)
    customer_response = requests.get(customers_api_url)
    necessaryitems_response = requests.get(necessaryitems_api_url)
    product_response = requests.get(product_api_url)

    # get url parse
    id_value = request.GET.get('id')

    # Check if the request was successful (status code 200)
    if appointment_response.status_code == 200:
        # Parse the JSON response
        appointment_data = appointment_response.json()
        customer_data = customer_response.json()
        necessaryitems_data = necessaryitems_response.json()
        product_data = product_response.json()

        #result = my_task.delay(3, 5)

        # Pass the data to the template for rendering
        return render(request, 'appointment_details.html', {'appointments': appointment_data, 'customers': customer_data, 'necessaryitems': necessaryitems_data, 'products': product_data})
    else:
        # Handle the case when the API request fails (e.g., return an error message)
        return render(request, 'error_template.html', {'message': 'Failed to fetch data from API'}) 

