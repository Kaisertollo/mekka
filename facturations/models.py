from django.db import models


class Invoice(models.Model):
    number = models.CharField(max_length=20)
    date = models.DateField()
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    products = models.ManyToManyField('Product', through='InvoiceProduct')

    def __str__(self):
        return f"Invoice {self.number}"


class Product(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class InvoiceProduct(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product} - Quantity: {self.quantity}"
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=200)
    # Add any other fields you need for the customer model

    def __str__(self):
        return self.name