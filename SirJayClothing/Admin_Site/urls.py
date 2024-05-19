from django.urls import path
from Admin_Site import views

urlpatterns = [ 
    path('manage_appointment/', views.ManageAppointmentPage, name='manage_appoinment'),
    path('manage_supplier/', views.SupplierPage, name='manage_supplier'),
    path('manage_services/', views.ServicesPage, name='manage_product'),
    path('manage_customer/', views.CustomerPage, name='manage_customer'),
    path('manage_customer_details/', views.CustomerDetailsPage, name='manage_customer_details'),
    path('manage_inventory/', views.InventoryPage, name='manage_inventory'),

    path('appointment_details/', views.AppointmentDetailsPage, name='appointment_details'),
    path('product_categories/', views.ProductCategoriesPage, name='product_categories'), 
     
]