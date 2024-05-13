import time
from django.shortcuts import render, redirect

from rest_framework import generics

from .models import Account, Customer, Appointment, Product, NecessaryItems, Supplier, Category
from .serializers import AccountSerializer, CustomerSerializer, ProductSerializer, \
    NecessaryItemsSerializer, SupplierSerializer, CategorySerializer, AppointmentSerializer  # Importing serializers for your models

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from rest_framework.authtoken.models import Token

class AccountList(generics.ListCreateAPIView):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

class CustomerList(generics.ListCreateAPIView):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

class AppointmentList(generics.ListCreateAPIView):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()

class AppointmentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()

class ProductList(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

class NecessaryItemsList(generics.ListCreateAPIView):
    serializer_class = NecessaryItemsSerializer
    queryset = NecessaryItems.objects.all()

class NecessaryItemsDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NecessaryItemsSerializer
    queryset = NecessaryItems.objects.all()

class SupplierList(generics.ListCreateAPIView):
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()

class SupplierDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()

class CategoryList(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

@csrf_exempt
def insert_customer_view(request):
    if request.method == 'POST':
        # Get form data
        fname = request.POST.get('fname')
        mname = request.POST.get('mname')
        lname = request.POST.get('lname')
        gender = request.POST.get('gender')
        phoneNum = request.POST.get('phoneNum')
        email = request.POST.get('email')

        # Save customer data to the database
        customer = Customer.objects.create(
            customerFname=fname,
            customerMname=mname,
            customerLname=lname,
            customerGender=gender,
            customerPhone=phoneNum,
            customerEmail=email,
        )

        # Return response
        #return JsonResponse({'message': 'Client_Site inserted successfully.'}, status=201)

        return redirect('/customer_add_customer')  # Replace '/appointment.html' with your desired URL

    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
 

@csrf_exempt
def insert_necessary_items(request):
    if request.method == 'POST':
        try:
             

            # Get form data
            appointment_selected_id = request.POST.get('appointmentselectedId')
            product_qty = int(request.POST.get('productQty'))
            product_id = int(request.POST.get('productId'))

            # Get the Product instance corresponding to the productId
            product_instance = Product.objects.get(id=product_id)
            appointment_instance = Appointment.objects.get(id=appointment_selected_id)

            if product_instance.productQty >= product_qty:
                # Save necessary items to the database

                # Check if the productName already exists in NecessaryItems
                existing_item = NecessaryItems.objects.filter(productName=product_instance,
                                                              appointmentName=appointment_instance).first()

                # Check if the productName already exists in NecessaryItems
                if existing_item:

                    existing_item.productQty += product_qty
                    existing_item.save()  # Save the updated quantity

                    #return JsonResponse({'error': 'This product is already added for this appointment.'}, status=400)

                else:
                    necessary_items = NecessaryItems.objects.create(
                        productQty=product_qty,
                        productName=product_instance,
                        appointmentName=appointment_instance,
                    )

                # Update productQty by subtracting product_qty
                product_instance.productQty -= product_qty
                product_instance.save()  # Save the updated quantity
                url_id = request.GET.get('id')   

                # Return success response
                return redirect(f'/admin_site/appointment_details?id={appointment_selected_id}')  # Replace with your desired URL

            else:
                # Return error response if quantity is insufficient
                return JsonResponse({'message': 'Insufficient product quantity.'}, status=400)

        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product does not exist.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

@csrf_exempt
def insert_appointment(request):
    if request.method == 'POST':
        # Get the current user
        user = request.user

        # Check if the user is authenticated
        if user.is_authenticated:
            # Get form data
            appointmentDate = request.POST.get('date')
            appointmentTime = request.POST.get('time')
            appointmentNotes = request.POST.get('notes') 

            # Get or create token for the user
            token, _ = Token.objects.get_or_create(user=user)

            # Get the customer using the token
            try:
                customer = Customer.objects.get(accountToken=token)
            except Customer.DoesNotExist:
                return JsonResponse({'error': 'Customer not found.'}, status=404)

            # Save appointment data to the database
            appointment = Appointment.objects.create(
                appointmentDate=appointmentDate,
                appointmentTime=appointmentTime,
                customerNotes=appointmentNotes, 
                customersName=customer,  # Pass the customer instance directly
            )

            # Redirect to the desired URL with the token as a query parameter
            return redirect(f'/success_page/?token={token.key}')

        else:
            return JsonResponse({'error': 'User is not authenticated.'}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    
 
@csrf_exempt
def delete_appointment(request):
    if request.method == 'POST':  
        # Get form data
        appointmentID = request.POST.get('appointmentID') 


        obj_to_delete = Appointment.objects.get(id=appointmentID)  # Replace obj_id with the ID of the object you want to delete
        obj_to_delete.delete()
            
        # Redirect to the desired URL with the token as a query parameter
        return redirect(f'/admin_site/manage_appointment/') 