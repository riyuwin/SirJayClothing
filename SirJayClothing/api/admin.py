from django.contrib import admin
from .models import Account, Customer, Appointment, Product, NecessaryItems, Supplier, Category


admin.site.register(Account)
admin.site.register(Customer)
admin.site.register(Appointment)
admin.site.register(Product)
admin.site.register(NecessaryItems)
admin.site.register(Supplier)
admin.site.register(Category)
