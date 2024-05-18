from django.urls import path
from .views import AccountList, AccountDetail, \
    CustomerList, CustomerDetail, \
    AppointmentList, AppointmentDetail, \
    ProductList, ProductDetail, \
    NecessaryItemsList, NecessaryItemsDetail, \
    SupplierList, SupplierDetail, \
    CategoryList, CategoryDetail, \
    ServicesList, ServicesDetail

from .models import Account, Customer, Appointment, Supply, NecessaryItems, Supplier, Category, Services

from . import views

urlpatterns = [
    #path('auth/account/', AccountList.as_view()),
    #path('auth/account/<int:pk>/', AccountDetail.as_view()),

    path('customer/', CustomerList.as_view()),
    path('customer/<int:pk>/', CustomerDetail.as_view()),

    path('appointment/appointment_details/', AppointmentList.as_view()),
    path('appointment/appointment_details/<int:pk>/', AppointmentDetail.as_view()),

    path('inventory/product/', ProductList.as_view()),
    path('inventory/product/<int:pk>/', ProductDetail.as_view()),
    path('inventory/necessaryitems/', NecessaryItemsList.as_view()),
    path('inventory/necessaryitems/<int:pk>/', NecessaryItemsDetail.as_view()),
    path('inventory/supplier/', SupplierList.as_view()),
    path('inventory/supplier/<int:pk>/', SupplierDetail.as_view()),
    path('inventory/category/', CategoryList.as_view()),
    path('inventory/category/<int:pk>/', CategoryDetail.as_view()),
    path('inventory/services/', ServicesList.as_view()),
    path('inventory/services/<int:pk>/', ServicesDetail.as_view()),

    path('account_registration/', views.insert_customer_view, name='account_registration'),

    path('insert_necessary_items/', views.insert_necessary_items, name='insert_necessary_items'),

    path('insert_appointment/', views.insert_appointment, name='insert_appointment'),
    path('delete_appointment/', views.delete_appointment, name='delete_appointment'),
    path('update_appointment/', views.update_appointment_status, name='update_appointment'),
 
    path('delete_category/', views.delete_categories, name='delete_category'),
    path('insert_category/', views.insert_product_categories, name='insert_category'),
    path('update_category/', views.update_product_categories, name='update_category'),

    
    path('insert_suppliers/', views.insert_supplier, name='insert_suppliers'),
    path('update_suppliers/', views.update_supplier, name='update_suppliers'),
    path('delete_supplier/', views.delete_supplier, name='delete_supplier'),

    
    path('insert_product/', views.insert_product, name='insert_product'),
    path('update_product/', views.update_product, name='update_product'),
    path('delete_product/', views.delete_product, name='delete_product'),

    path('insert_services/', views.insert_services, name='insert_product'),
    path('update_services/', views.update_services, name='update_services'),
    path('delete_services/', views.delete_services, name='delete_services'),
]