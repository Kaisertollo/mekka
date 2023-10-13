from facturations.models import *
from facturations.serializers import *
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import json
import bcrypt
from facturations.utils import generate_code,Send_wp,hashPassword,send_sms,sendMail

class CustomerAPI(APIView):
    def get(self, request):
        customers = Customer.objects.all()
        # Convert the customer data to JSON or any desired format
        data = [{'id':customer.id,'name': customer.name, 'email': customer.email, 'address': customer.address,'token': customer.token} for customer in customers]
        return Response(data)
    def post(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        address = request.data.get('address')
        customer = Customer.objects.create(name=name, email=email, address=address)
        return Response({'id': customer.id, 'name': customer.name, 'email': customer.email,'address': customer.address})
class CustomerById(APIView):
    def get(self, request,customer_id):
        customer = Customer.objects.get(id = customer_id)
        data = {'id':customer.id,'name': customer.name, 'email': customer.email, 'address': customer.address}
        return Response(data)
    def put(self, request, customer_id):
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return JsonResponse({'error': 'Invoice not found'}, status=status.HTTP_404_NOT_FOUND)

        customer = Customer.objects.get(id=customer_id)
        customer.name = request.data.get('name')
        customer.email = request.data.get('email')
        customer.address = request.data.get('address')
        customer.save()
        return Response(customer)
    def delete(self, request, customer_id):
        try:
            customer = Customer.objects.get(id=customer_id)
            customer.delete()
            return Response({'status': 'deleted'})
        except Invoice.DoesNotExist:
            return JsonResponse({'error': 'Invoice not found'}, status=status.HTTP_404_NOT_FOUND)

class CustomerTokenAPI(APIView):
    def post(self, request):
        token = request.data.get('token')
        customer_id = request.data.get('id')
        customer = Customer.objects.get(id=customer_id)
        customer.token = token
        customer.save()
        return Response({'state': "success"})
class CustomerApiLogin(APIView):
    def post(self, request):
        p = request.data.get('phone')
        c = Customer.objects.filter(phone = p).first()
        if c:
            if not c.first_connection_done:
                code = generate_code()
                Send_wp(p,code)
                sendMail(code,c.email)
                return Response({'id':c.id,'first':True,'code':code})
            else:
                return Response({'id':c.id,'first':False,'code':0})
        else:
            return Response({'id':0,'first':False,'code':0})

class CustomerCreatePassword(APIView):
    def post(self, request):
        p = request.data.get('phone')
        pwd = request.data.get('pwd')
        c = Customer.objects.filter(phone = p).first()
        if c:
            c.pwd = hashPassword(pwd)
            c.first_connection_done = True
            c.save()
            return Response({'id':c.id,'code':"succes"})
        else:
            return Response({'id':0,'code':"FAILURE"})
class CustomerLoginPassword(APIView):
    def post(self, request):
        p = request.data.get('phone')
        pwd = request.data.get('pwd')
        c = Customer.objects.filter(phone = p).first()
        if c:
            if c.pwd == f"b'{hashPassword(pwd).decode('utf-8')}'":
                return Response({'id':c.id,'code':"succes"})
            else:
                return Response({'id':0,'code':"FAILURE"})
        else:
            return Response({'id':0,'code':"FAILURE"})

