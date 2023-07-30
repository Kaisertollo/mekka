from facturations.models import *
from facturations.serializers import InvoiceSerializer
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from facturations.utils import generate_code,Send_wp
import json

class CorporateAPI(APIView):
    def get(self, request):
        corporates = Corporate.objects.all()
        data = [{'id': corporate.id, 'name': corporate.name, 'email': corporate.email, 'address': corporate.address} for corporate in corporates]
        return Response(data)

    def post(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        address = request.data.get('address')
        phone = request.data.get('phone')
        corporate = Corporate.objects.create(name=name, email=email, address=address, phone=phone)
        return Response({'id': corporate.id, 'name': corporate.name, 'email': corporate.email, 'address': corporate.address, 'phone': corporate.phone})

class CorporateById(APIView):
    def get(self, request, corporate_id):
        corporate = Corporate.objects.get(id=corporate_id)
        data = {'id': corporate.id, 'name': corporate.name, 'email': corporate.email, 'address': corporate.address, 'phone': corporate.phone}
        return Response(data)

    def put(self, request, corporate_id):
        try:
            corporate = Corporate.objects.get(id=corporate_id)
        except Corporate.DoesNotExist:
            return JsonResponse({'error': 'Corporate not found'}, status=status.HTTP_404_NOT_FOUND)

        corporate.name = request.data.get('name')
        corporate.email = request.data.get('email')
        corporate.address = request.data.get('address')
        corporate.phone = request.data.get('phone')
        corporate.save()
        return Response({'id': corporate.id, 'name': corporate.name, 'email': corporate.email, 'address': corporate.address, 'phone': corporate.phone})

    def delete(self, request, corporate_id):
        try:
            corporate = Corporate.objects.get(id=corporate_id)
            corporate.delete()
            return Response({'status': 'deleted'})
        except Corporate.DoesNotExist:
            return JsonResponse({'error': 'Corporate not found'}, status=status.HTTP_404_NOT_FOUND)
class CorporateApiLogin(APIView):
    def post(self, request):
        p = request.data.get('phone')
        c = Corporate.objects.filter(phone = p).first()
        if c:
            code = "0000"
            Send_wp(p,code)
            return Response({'id':c.id,'code': code,'name':c.name,'phone':c.phone,'id':c.id})
        else:
            return Response({'id':0,'code': "0",'name':"agent.name",'phone':"agent.phone",'id':"agent.id"})
