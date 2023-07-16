from rest_framework import serializers
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class InvoiceProductSerializer(serializers.ModelSerializer):
   product = ProductSerializer(read_only=True)
   
   class Meta:
        model = InvoiceProduct
        fields = ('id','quantity','product')


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class CorporateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corporate
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    invoice_product = InvoiceProductSerializer(many=True)

    class Meta:
        model = Invoice
        fields = '__all__'

