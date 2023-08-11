from django.db import models


class Invoice(models.Model):
    number = models.CharField(max_length=20)
    date = models.DateField()
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    agent = models.ForeignKey('Agent', on_delete=models.CASCADE,null=True,blank=True)
    corporate = models.ForeignKey('Corporate', on_delete=models.CASCADE,null=True)
    payed = models.BooleanField(default=False)
    total_amount = 0
    invoice_product = list()

    def calculate_total_amount(self):
        invoice_products = InvoiceProduct.objects.filter(invoice=self)
        total = sum([invoice_product.quantity * invoice_product.product.price for invoice_product in invoice_products])
        self.total_amount = total
        return total
    def __str__(self):
        return f"Invoice {self.number}"


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.name


class InvoiceProduct(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    def __str__(self):
        return f"{self.product} - Quantity: {self.quantity}"
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=50,unique=True)
    token = models.CharField(max_length=250)
    # Add any other fields you need for the customer model

    def __str__(self):
        return self.name

class Corporate(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=50,unique=True)
    # Add any other fields you need for the customer model

    def __str__(self):
        return self.name
class Agent(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=50,unique=True)
    code = models.CharField(max_length=10,unique=True)
    # Add any other fields you need for the customer model

    def __str__(self):
        return self.name
