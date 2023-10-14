from facturations.models import *
from facturations.serializers import InvoiceSerializer
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from facturations.utils import generate_code,Send_wp,sendMail,hashPassword
import json

class AgentAPI(APIView):
    def get(self, request):
        agents = Agent.objects.all()
        data = [{'id': agent.id, 'name': agent.name, 'email': agent.email, 'address': agent.address, 'phone': agent.phone, 'code': agent.code} for agent in agents]
        return Response(data)

    def post(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        address = request.data.get('address')
        phone = request.data.get('phone')
        code = request.data.get('code')
        agent = Agent.objects.create(name=name, email=email, address=address, phone=phone, code=code)
        return Response({'id': agent.id, 'name': agent.name, 'email': agent.email, 'address': agent.address, 'phone': agent.phone, 'code': agent.code})

class AgentById(APIView):
    def get(self, request, agent_id):
        agent = Agent.objects.get(id=agent_id)
        data = {'id': agent.id, 'name': agent.name, 'email': agent.email, 'address': agent.address, 'phone': agent.phone, 'code': agent.code}
        return Response(data)

    def put(self, request, agent_id):
        try:
            agent = Agent.objects.get(id=agent_id)
        except Agent.DoesNotExist:
            return JsonResponse({'error': 'Agent not found'}, status=status.HTTP_404_NOT_FOUND)

        agent.name = request.data.get('name')
        agent.email = request.data.get('email')
        agent.address = request.data.get('address')
        agent.phone = request.data.get('phone')
        agent.code = request.data.get('code')
        agent.save()
        return Response({'id': agent.id, 'name': agent.name, 'email': agent.email, 'address': agent.address, 'phone': agent.phone, 'code': agent.code})

    def delete(self, request, agent_id):
        try:
            agent = Agent.objects.get(id=agent_id)
            agent.delete()
            return Response({'status': 'deleted'})
        except Agent.DoesNotExist:
            return JsonResponse({'error': 'Agent not found'}, status=status.HTTP_404_NOT_FOUND)
        
class AgentTokenAPI(APIView):
    def post(self, request):
        token = request.data.get('token')
        agent_id = request.data.get('id')
        agent = Agent.objects.get(id=agent_id)
        agent.token = token
        agent.save()
        return Response({'state': "success"})
class AgentApiLogin(APIView):
    def post(self, request):
        p = request.data.get('phone')
        a = Agent.objects.filter(phone = p).first()
        if a:
            if not a.first_connection_done:
                code = generate_code()
                Send_wp(p,code)
                sendMail(code,a.email)
                return Response({'id':a.id,'first':True,'code':code})
            else:
                return Response({'id':a.id,'first':False,'code':0})
        else:
            return Response({'id':0,'first':False,'code':0})

class AgentCreatePassword(APIView):
    def post(self, request):
        p = request.data.get('phone')
        pwd = request.data.get('pwd')
        a = Agent.objects.filter(phone = p).first()
        if a:
            a.pwd = hashPassword(pwd)
            a.first_connection_done = True
            a.save()
            return Response({'id':a.id,'code':"succes"})
        else:
            return Response({'id':0,'code':"FAILURE"})
class AgentLoginPassword(APIView):
    def post(self, request):
        p = request.data.get('phone')
        pwd = request.data.get('pwd')
        a = Agent.objects.filter(phone = p).first()
        if a:
            if a.pwd == f"b'{hashPassword(pwd).decode('utf-8')}'":
                return Response({'id':a.id,'code':"succes"})
            else:
                return Response({'id':0,'code':"FAILURE"})
        else:
            return Response({'id':0,'code':"FAILURE"})