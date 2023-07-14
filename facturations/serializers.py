from rest_framework import serializers
from .models import Invoice, Product, InvoiceProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name')


class InvoiceProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = InvoiceProduct
        fields = ('product', 'quantity', 'price')


class InvoiceSerializer(serializers.ModelSerializer):
    products = InvoiceProductSerializer(many=True)

    class Meta:
        model = Invoice
        fields = ('id', 'number', 'date', 'customer', 'total_amount', 'products')
