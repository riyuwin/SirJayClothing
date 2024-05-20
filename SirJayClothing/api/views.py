import time
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from rest_framework import generics

from .models import Account, Customer, Appointment, Supply, NecessaryItems, Supplier, Category, Services, AppointmentQuery
from .serializers import AccountSerializer, CustomerSerializer, ProductSerializer, \
    NecessaryItemsSerializer, SupplierSerializer, CategorySerializer, AppointmentSerializer, ServicesSerializer, AppointmentQuerySerializer  # Importing serializers for your models

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
    queryset = Supply.objects.all()

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Supply.objects.all()

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


class ServicesList(generics.ListCreateAPIView):
    serializer_class = ServicesSerializer
    queryset = Services.objects.all()

class ServicesDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ServicesSerializer
    queryset = Services.objects.all()

class AppointmentQueryList(generics.ListCreateAPIView):
    serializer_class = AppointmentQuerySerializer
    queryset = AppointmentQuery.objects.all()

class AppointmentQueryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AppointmentQuerySerializer
    queryset = AppointmentQuery.objects.all()


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

        return redirect('/customer_add_customer')  

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
            product_instance = Supply.objects.get(id=product_id)
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
                return redirect(f'/admin_site/appointment_details?id={appointment_selected_id}')  

            else:
                # Return error response if quantity is insufficient
                return JsonResponse({'message': 'Insufficient product quantity.'}, status=400)

        except Supply.DoesNotExist:
            return JsonResponse({'error': 'Product does not exist.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


@csrf_exempt
def update_necessary_items(request):
    if request.method == 'POST':
        user = request.user

        if user.is_authenticated:  
            # Get form data
            necessaryitemsID = request.POST.get('necessaryitemsID')
            editproductId = int(request.POST.get('editproductId'))
            editproductQty = int(request.POST.get('editproductQty')) 
            appointmentID = int(request.POST.get('appointmentID'))  
 
            necessaryItems = get_object_or_404(NecessaryItems, id=necessaryitemsID) 
            appointment_instance = Supply.objects.get(id=editproductId) 

            # Get the Product instance corresponding to the productId
            product_instance = Supply.objects.get(id=editproductId)
            
            if necessaryItems.productQty <= editproductQty:
                product_added = editproductQty - necessaryItems.productQty  

                product_instance.productQty += product_added
                product_instance.save()  # Save the updated quantity
                
            elif necessaryItems.productQty >= editproductQty:
                if product_instance.productQty >= editproductQty:                
                    # Update productQty by subtracting product_qty
                    product_subtracted = necessaryItems.productQty - editproductQty 

                    product_instance.productQty -= product_subtracted
                    product_instance.save()  # Save the updated quantity

            necessaryItems.productQty = editproductQty
            necessaryItems.productName = appointment_instance 
            necessaryItems.save()

            return redirect(f'/admin_site/appointment_details/?id={appointmentID}')
        else:
            return JsonResponse({'error': 'User is not authenticated.'}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

@csrf_exempt
def delete_necessary_items(request):
    if request.method == 'POST':  
        # Get form data
        necessaryID = request.POST.get('deletecategoryID') 
        appointmentName = request.POST.get('appointmentName') 

        print(f'NecessaryID: {necessaryID} |')

        obj_to_delete = NecessaryItems.objects.get(id=necessaryID)  
        obj_to_delete.delete()
            
        # Redirect to the desired URL with the token as a query parameter
        return redirect(f'/admin_site/appointment_details/?id={appointmentName}') 



@csrf_exempt
def insert_appointment(request):
    if request.method == 'POST':
        # Get the current user
        user = request.user

        # Check if the user is authenticated
        if user.is_authenticated:
            # Get form data
            services_selector = request.POST.get('servicesSelector')
            appointment_date = request.POST.get('date')
            appointment_time = request.POST.get('time')
            appointment_qty = request.POST.get('quantity')
            appointment_notes = request.POST.get('notes') 

            # Validate the received data
            if not all([services_selector, appointment_date, appointment_qty, appointment_time]):
                return JsonResponse({'error': 'Missing required fields.'}, status=400)

            # Get or create token for the user
            token, _ = Token.objects.get_or_create(user=user)

            try: 
                customer = Customer.objects.get(accountToken=token.key)

                # Get the selected service
                service = Services.objects.get(id=services_selector)

                print(customer.id, 'asda')
                print(service.id, 'service')

                # Default status
                default_status = 'Pending'

                # Check for existing appointment
                existing_appointment = Appointment.objects.filter(customersName=customer.id, appointmentServices=service.id, appointmentStatus=default_status).exists()

                if existing_appointment:
                    return JsonResponse({'error': 'An appointment with this service already exists for this customer.'}, status=400) 

                # Save appointment data to the database
                appointment = Appointment.objects.create(
                    appointmentDate=appointment_date,
                    appointmentTime=appointment_time,
                    customerNotes=appointment_notes,  
                    appointmentStatus=default_status,
                    appointmentQty=appointment_qty,
                    customersName=customer,   
                    appointmentServices=service,
                )

                # Redirect to the desired URL with the token as a query parameter
                return redirect(f'/success_page/?token={token.key}')

            except Customer.DoesNotExist:
                return JsonResponse({'error': 'Customer not found.'}, status=404)
            except Services.DoesNotExist:
                return JsonResponse({'error': 'Service not found.'}, status=404)

        else:
            return JsonResponse({'error': 'User is not authenticated.'}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
        
@csrf_exempt
def delete_appointment(request):
    if request.method == 'POST':  
        # Get form data
        appointmentID = request.POST.get('appointmentID') 


        obj_to_delete = Appointment.objects.get(id=appointmentID)   
        obj_to_delete.delete()
            
        # Redirect to the desired URL with the token as a query parameter
        return redirect(f'/admin_site/manage_appointment/') 


@csrf_exempt
def delete_categories(request):
    if request.method == 'POST':  
        # Get form data
        categoryID = request.POST.get('deletecategoryID')  

        obj_to_delete = Category.objects.get(id=categoryID)   
        obj_to_delete.delete()
            
        # Redirect to the desired URL with the token as a query parameter
        return redirect(f'/admin_site/product_categories/') 
    

@csrf_exempt
def insert_product_categories(request):
    if request.method == 'POST':
        user = request.user

        if user.is_authenticated:
            productCategoriesName = request.POST.get('productCategory')
            productDescription = request.POST.get('description')

            if not productCategoriesName:
                return JsonResponse({'error': 'Missing required fields.'}, status=400)

            try:
                token, _ = Token.objects.get_or_create(user=user)

                # Check for existing category
                existing_category = Category.objects.filter(categoryName=productCategoriesName).exists()
                if existing_category:
                    return JsonResponse({'message': 'A category with this name already exists.'}, status=200)

                category = Category.objects.create(
                    categoryName=productCategoriesName,
                    categoryDesc=productDescription,
                )

                #return JsonResponse({'redirect_url': '/admin_site/product_categories/'})
                return redirect(f'/admin_site/product_categories/') 

            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)

        else:
            return JsonResponse({'error': 'User is not authenticated.'}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

@csrf_exempt
def update_product_categories(request):
    if request.method == 'POST':
        # Get the current user
        user = request.user

        # Check if the user is authenticated
        if user.is_authenticated:
            # Get form data
            editcategoryID = request.POST.get('editcategoryID')
            productCategory = request.POST.get('productCategory')
            productDescription = request.POST.get('description') 

            # Get the existing category object or return 404 if not found
            category = get_object_or_404(Category, id=editcategoryID)

            # Update category attributes
            category.categoryName = productCategory
            category.categoryDesc = productDescription
            category.save()

            # Redirect or return success response
            return redirect(f'/admin_site/product_categories/')
            #return JsonResponse({'success': 'Category updated successfully.'})
        else:
            return JsonResponse({'error': 'User is not authenticated.'}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


@csrf_exempt
def insert_supplier(request):
    if request.method == 'POST':
        # Get the current user
        user = request.user

        # Check if the user is authenticated
        if user.is_authenticated:
            # Get form data
            supplierNameText = request.POST.get('supplierName')
            contactNumber = request.POST.get('contactNumber') 
            emailAdd = request.POST.get('emailAdd') 
            address = request.POST.get('supplierAddress') 

            # Get or create token for the user
            token, _ = Token.objects.get_or_create(user=user)
 
            # Check for existing category
            existing_category = Supplier.objects.filter(supplierName=supplierNameText).exists()
            if existing_category:
                return JsonResponse({'message': 'A supplier with this name already exists.'}, status=200)

 
            # Save appointment data to the database
            supplier = Supplier.objects.create(
                supplierName=supplierNameText,
                contactNumber=contactNumber, 
                supplierEmail=emailAdd, 
                supplierAddress=address, 
            )

            # Redirect to the desired URL with the token as a query parameter
            return redirect(f'/admin_site/manage_supplier/')

        else:
            return JsonResponse({'error': 'User is not authenticated.'}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

@csrf_exempt
def update_supplier(request):
    if request.method == 'POST':
        # Get the current user
        user = request.user

        # Check if the user is authenticated
        if user.is_authenticated:
            # Get form data
            suppliercategoryID = request.POST.get('suppliercategoryID')
            supplierName = request.POST.get('supplierName')
            contactNumber = request.POST.get('contactNumber')
            emailAdd = request.POST.get('emailAdd') 
            address = request.POST.get('supplierAddress') 

            # Get the existing category object or return 404 if not found
            category = get_object_or_404(Supplier, id=suppliercategoryID)

            # Update category attributes 
            category.supplierName = supplierName
            category.contactNumber = contactNumber
            category.supplierEmail = emailAdd
            category.supplierAddress = address
            category.save()

            # Redirect or return success response
            return redirect(f'/admin_site/manage_supplier/')
            #return JsonResponse({'success': 'Category updated successfully.'})
        else:
            return JsonResponse({'error': 'User is not authenticated.'}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

@csrf_exempt
def delete_supplier(request):
    if request.method == 'POST':  
        # Get form data
        categoryID = request.POST.get('deletecategoryID')  

        obj_to_delete = Supplier.objects.get(id=categoryID)   
        obj_to_delete.delete()
            
        # Redirect to the desired URL with the token as a query parameter
        return redirect(f'/admin_site/manage_supplier/') 

@csrf_exempt
def insert_product(request):
    if request.method == 'POST':
        user = request.user

        if user.is_authenticated:
            productName = request.POST.get('productName')
            productQty = request.POST.get('productQty') 
            productUnit = request.POST.get('productUnit') 
            productPrice = request.POST.get('productPrice') 
            productCategory = request.POST.get('productCategory') 
            supplierSelector = request.POST.get('supplierSelector') 

            if not all([productName, productQty, productUnit, productPrice, productCategory, supplierSelector]):
                return JsonResponse({'error': 'Missing required fields.'}, status=400)

            try:
                token, _ = Token.objects.get_or_create(user=user)

                supplier_id = int(supplierSelector)
                supplier_instance = Supplier.objects.get(id=supplier_id)

                category_id = int(productCategory)
                category_instance = Category.objects.get(id=category_id)

                # Check for existing product
                existing_product = Supply.objects.filter(
                    productName=productName,
                    productCategory=category_instance,
                    supplierName=supplier_instance
                ).exists()

                if existing_product:
                    return JsonResponse({'message': 'A product with the same name, category, and supplier already exists.'}, status=200)

                product = Supply.objects.create(
                    productName=productName,
                    productQty=productQty,
                    productUnit=productUnit,
                    productPrice=productPrice,
                    productCategory=category_instance,
                    supplierName=supplier_instance,
                )

                return redirect(f'/admin_site/manage_inventory/')

            except Supplier.DoesNotExist:
                return JsonResponse({'error': 'Supplier not found.'}, status=404)
            except Category.DoesNotExist:
                return JsonResponse({'error': 'Category not found.'}, status=404)
        else:
            return JsonResponse({'error': 'User is not authenticated.'}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

@csrf_exempt
def update_product(request):
    if request.method == 'POST':
        # Get the current user
        user = request.user

        # Check if the user is authenticated
        if user.is_authenticated:
            # Get form data
            productId = request.POST.get('productIDSelected')   
            productName = request.POST.get('productName')
            productQty = request.POST.get('productQty') 
            productUnit = request.POST.get('productUnit') 
            productPrice = request.POST.get('productPrice') 
            productCategory = request.POST.get('productCategory') 
            supplierSelector = request.POST.get('supplierSelector')    
 
            supplier_id = int(supplierSelector)  
            supplier_instance = Supplier.objects.get(id=supplier_id)

            category_id = int(productCategory)   
            category_instance = Category.objects.get(id=category_id)
            
            print(productId)

            # Get the existing product object or return 404 if not found
            supply = get_object_or_404(Supply, id=productId)

            # Update product attributes 
            supply.productName = productName
            supply.productQty = productQty
            supply.productUnit = productUnit
            supply.productPrice = productPrice
            supply.supplierName = supplier_instance
            supply.productCategory = category_instance
            supply.save()

            # Redirect or return success response
            return redirect('/admin_site/manage_inventory/')  # Redirect URL corrected
        else:
            return JsonResponse({'error': 'User is not authenticated.'}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    

@csrf_exempt
def delete_product(request):
    if request.method == 'POST':  
        # Get form data
        categoryID = request.POST.get('deletecategoryID')  

        obj_to_delete = Supply.objects.get(id=categoryID)  
        obj_to_delete.delete()
            
        # Redirect to the desired URL with the token as a query parameter
        return redirect(f'/admin_site/manage_inventory/') 
    

@csrf_exempt
def delete_customer(request):
    if request.method == 'POST':  
        # Get form data
        categoryID = request.POST.get('deletecategoryID')  

        obj_to_delete = Supply.objects.get(id=categoryID)  
        obj_to_delete.delete()
            
        # Redirect to the desired URL with the token as a query parameter
        return redirect(f'/admin_site/manage_customer/') 


@csrf_exempt
def insert_services(request):
    if request.method == 'POST':
        user = request.user

        if user.is_authenticated:
            name = request.POST.get('clothName')
            school = request.POST.get('schoolName') 
            price = request.POST.get('servicePrice')
            description = request.POST.get('description')
            
            # Check if an image is uploaded
            clothImg = request.FILES.get('imgClothInput')

            # Get or create token for the user
            token, _ = Token.objects.get_or_create(user=user)

            # Check for existing category
            existing_category = Services.objects.filter(clothOffered=name,clothforSchool=school).exists()
            if existing_category:
                return JsonResponse({'message': 'A supplier with this name already exists.'}, status=200)


            # Save service data to the database
            service = Services.objects.create(
                clothOffered=name,
                clothforSchool=school, 
                clothPrice=price,
                clothNotes=description,
                image=clothImg,  
            )

            # Redirect to the desired URL
            return redirect(f'/admin_site/manage_services/')
        else:
            return JsonResponse({'error': 'User is not authenticated.'}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

@csrf_exempt
def update_services(request):
    if request.method == 'POST':
        user = request.user

        if user.is_authenticated:
            serviceId = request.POST.get('servicesIDSelected')
            name = request.POST.get('clothName')
            school = request.POST.get('schoolName') 
            price = request.POST.get('servicePrice')
            description = request.POST.get('description')

            services = get_object_or_404(Services, id=serviceId)

            services.clothOffered = name
            services.clothforSchool = school 
            services.clothPrice = price
            services.clothNotes = description

            if 'imgClothInput' in request.FILES:
                services.image = request.FILES['imgClothInput']

            services.save()

            return redirect('/admin_site/manage_services/')
        else:
            return JsonResponse({'error': 'User is not authenticated.'}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

@csrf_exempt
def delete_services(request):
    if request.method == 'POST':  
        # Get form data
        categoryID = request.POST.get('deletecategoryID')  

        obj_to_delete = Services.objects.get(id=categoryID)  
        obj_to_delete.delete()
            
        # Redirect to the desired URL with the token as a query parameter
        return redirect(f'/admin_site/manage_services/') 

@csrf_exempt
def update_appointment_status(request):
    if request.method == 'POST':
        user = request.user

        if user.is_authenticated:
            url_id = request.GET.get('id')

            if not url_id:
                return JsonResponse({'error': 'ID parameter is missing.'}, status=400)

            status = request.POST.get('status')

            if not status:
                return JsonResponse({'error': 'Status parameter is missing.'}, status=400)

            appointment = get_object_or_404(Appointment, id=url_id)

            appointment.appointmentStatus = status
            appointment.save()

            return redirect(f'/admin_site/appointment_details/?id={url_id}')
        else:
            return JsonResponse({'error': 'User is not authenticated.'}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


@csrf_exempt
def insert_appointment_query(request):
    if request.method == 'POST':
        user = request.user

        if user.is_authenticated: 
            appointmentID = request.POST.get('appointmentID')
            query = request.POST.get('message') 

            url_id = request.GET.get('id')   

            # Determine if the user is admin or customer
            user_type = 'Admin' if user.is_staff or user.is_superuser else 'Customer'

            # Get the Appointment instance using the ID
            appointment_instance = Appointment.objects.get(id=appointmentID)

            # Save service data to the database
            service = AppointmentQuery.objects.create(
                appointmentName=appointment_instance,   
                userFeedback=user_type,  
                message=query,  
            )

            if user_type == "Customer":
                # Redirect to the desired URL
                return redirect(f'/customer_information/?id={url_id}')
            elif user_type == "Admin":
                return redirect(f'/admin_site/ppointment_details/?id={url_id}')
            
        else:
            return JsonResponse({'error': 'User is not authenticated.'}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

def admin_account_checker(request): 
    user = request.user

    if user.is_authenticated:
        # Determine if the user is admin or customer
        user_type = 'Admin' if user.is_staff or user.is_superuser else 'Customer'

        if user_type != "Admin":
            return redirect('/authorized_template/')
    

def customer_account_checker(request): 
    user = request.user

    if user.is_authenticated:
        # Determine if the user is admin or customer
        user_type = 'Admin' if user.is_staff or user.is_superuser else 'Customer'

        if user_type != "Customer":
            return redirect('/authorized_template/')
    return None  # Return None if the user is an admin or if the user is not authenticated

def authorized_template_page(request):
    return render(request, 'authorized_template.html', {'message': 'Authorized user only.'})
