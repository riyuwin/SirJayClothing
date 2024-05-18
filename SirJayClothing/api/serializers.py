from rest_framework import serializers
from .models import Account, Customer, Appointment, Supply, NecessaryItems, Supplier, Category, Services
# This section converts the model object into JSON format, at vice versa

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('__all__')

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('__all__')

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('__all__')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supply
        fields = ('__all__')

class NecessaryItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NecessaryItems
        fields = ('__all__')

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ('__all__')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('__all__')


class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = ('__all__')