from django.contrib import admin
from .models import Account, Customer, Appointment, Supply, NecessaryItems, Supplier, Category, Services, AppointmentQuery


admin.site.register(Account)
admin.site.register(Customer)
admin.site.register(Appointment)
admin.site.register(Supply)
admin.site.register(NecessaryItems)
admin.site.register(Supplier)
admin.site.register(Category)
admin.site.register(Services)
admin.site.register(AppointmentQuery)
