from django.db import models


class Account(models.Model):
    accountEmail = models.CharField(max_length=100)
    accountPassword = models.CharField(max_length=100)
    ACCOUNT_ROLE_CHOICES = (
        ('Client_Site', 'Client_Site'),
        ('Admin', 'Admin'),
    )
    accountRole = models.CharField(max_length=20, choices=ACCOUNT_ROLE_CHOICES, default='Client_Site')
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.accountEmail} - {self.accountRole}'


class Customer(models.Model):
    #customerAccount = models.ForeignKey(Account, on_delete=models.CASCADE)

    customerFname = models.CharField(max_length=100)
    customerMname = models.CharField(max_length=100)
    customerLname = models.CharField(max_length=100)

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    customerGender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='Male')
    customerPhone = models.CharField(max_length=50)
    customerEmail = models.EmailField(max_length=254)
    customerBirthdate = models.DateField()
    customerAddress = models.CharField(max_length=500)
    date_added = models.DateField(auto_now_add=True)

    accountToken = models.CharField(max_length=500, blank=True, null=True)  # Make categoryDesc optional

    def __str__(self):
        return f'{self.customerLname}, {self.customerFname} {self.customerMname}'


class Services(models.Model):
    clothOffered = models.CharField(max_length=500)
    clothforSchool = models.CharField(max_length=500) 
    clothPrice = models.IntegerField() 
    clothNotes = models.CharField(max_length=1000) 
    date_added = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)  # New field for image


    def __str__(self):
        return f'{self.clothforSchool} - {self.clothOffered}'


class Appointment(models.Model):
    customersName = models.ForeignKey(Customer, on_delete=models.CASCADE)

    appointmentDate = models.DateField()
    appointmentTime = models.TimeField()
    appointmentServices = models.ForeignKey(Services, on_delete=models.CASCADE)
    appointmentQty = models.IntegerField()
    customerNotes = models.CharField(max_length=200, blank=True, null=True)  # Make categoryDesc optional

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    )

    appointmentStatus = models.CharField(max_length=40, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Set appointment: {self.customersName} - {self.appointmentDate} | {self.appointmentTime}"


class Supplier(models.Model):
    supplierName = models.CharField(max_length=100)
    contactNumber = models.CharField(max_length=100)
    supplierEmail = models.EmailField() 
    supplierAddress = models.CharField(max_length=500)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.supplierName


class Category(models.Model):
    categoryName = models.CharField(max_length=100)
    categoryDesc = models.CharField(max_length=500, blank=True, null=True)  # Make categoryDesc optional

    def __str__(self):
        return self.categoryName


class Supply(models.Model):
    supplierName = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    productCategory = models.ForeignKey(Category, on_delete=models.CASCADE)

    productName = models.CharField(max_length=100)

    UNITS_CHOICES = (
        ('Pieces', 'Pieces'),
        ('Inches', 'Inches'),
        ('Meters', 'Meters'),
        ('Feet', 'Feet'), 
        ('Boxes', 'Boxes'),
        ('Dozen', 'Dozen'),
        ('Yards', 'Yards'),
        ('Pounds', 'Pounds'),
        ('Bundles', 'Bundles'),
        ('Gallons', 'Gallons'),
    )

    #productUnit = models.CharField(max_length=100)
    productQty = models.IntegerField()
    productUnit = models.CharField(max_length=100, choices=UNITS_CHOICES, default='Pieces')
    productPrice = models.IntegerField()
    productDescp = models.CharField(max_length=500, blank=True, null=True)  # Make categoryDesc optional
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.productName


class NecessaryItems(models.Model):
    productName = models.ForeignKey(Supply, on_delete=models.CASCADE)
    productQty = models.IntegerField()
    appointmentName = models.ForeignKey(Appointment, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.productName} - {self.appointmentName}'


class AppointmentQuery(models.Model):
    appointmentName = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)
    message = models.CharField(max_length=500)

    USER_CHOICES = (
        ('Admin', 'Admin'),
        ('Customer', 'Customer'), 
    )

    userFeedback = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.appointmentName}'
