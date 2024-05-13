from django.urls import path
from .views import AccountList, AccountDetail, \
    CustomerList, CustomerDetail, \
    AppointmentList, AppointmentDetail, \
    ProductList, ProductDetail, \
    NecessaryItemsList, NecessaryItemsDetail, \
    SupplierList, SupplierDetail, \
    CategoryList, CategoryDetail

from .models import Account, Customer, Appointment, Product, NecessaryItems, Supplier, Category

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

    path('account_registration/', views.insert_customer_view, name='account_registration'),

    path('insert_necessary_items/', views.insert_necessary_items, name='insert_necessary_items'),
    path('insert_appointment/', views.insert_appointment, name='insert_appointment'),
]