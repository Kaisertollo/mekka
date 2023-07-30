from facturations.models import *
from facturations.serializers import InvoiceSerializer
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from facturations.utils import generate_code,Send_wp
import json

class ProductAPI(APIView):
    def get(self, request):
        products = Product.objects.all()
        data = [{'id': product.id, 'name': product.name, 'price': product.price} for product in products]
        return Response(data)

    def post(self, request):
        name = request.data.get('name')
        price = request.data.get('price')
        product = Product.objects.create(name=name, price=price)
        return Response({'id': product.id, 'name': product.name, 'price': product.price})

class ProductById(APIView):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        data = {'id': product.id, 'name': product.name, 'price': product.price}
        return Response(data)

    def put(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        product.name = request.data.get('name')
        product.price = request.data.get('price')
        product.save()
        return Response({'id': product.id, 'name': product.name, 'price': product.price})

    def delete(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            return Response({'status': 'deleted'})
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)