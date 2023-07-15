from rest_framework import serializers
from .models import Invoice, Product, InvoiceProduct, Customer

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class InvoiceProductSerializer(serializers.ModelSerializer):
   product = ProductSerializer(read_only=True)
   
   class Meta:
        model = InvoiceProduct
        fields = ('id','quantity','product')



class InvoiceSerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField()
    invoice_product = InvoiceProductSerializer(many=True)

    class Meta:
        model = Invoice
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
