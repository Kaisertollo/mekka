from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import ListView, DetailView, View
from .models import *
from .serializers import *
import requests
import json
from facturations.utils import generate_code,Send_wp,create_marchand
from django.views.decorators.csrf import csrf_exempt
import random
import string
from pyfcm import FCMNotification
import facturations.api.invoices_api as invoice_api


def send_notif(token,title,body,data_payload):
    # Configure your Firebase Cloud Messaging server key
    api_key = "AAAA0IjcuIQ:APA91bE75plgpm8K-9bzimA1GUY-fx7lu1AJwhaoJPW_5EOKAD6djPw-l1BTUHGrbMPdf7R_MH2VNYg0Trpbc9ZzYSnkxZSnMo44MHfagRjvOoqtNk12Ec8jFI570Fofht4CIEMEjCAh"

    # Initialize the FCMNotification object
    push_service = FCMNotification(api_key=api_key)
    # Send a message to a specific device
    registration_id =token
    message_title = title
    message_body = body
    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body,data_message=data_payload)
    print(result)
class AgentAPI(APIView):
    def get(self, request):
        agents = Agent.objects.all()
        # Convert the customer data to JSON or any desired format
        data = [{'id':agent.id,'name': agent.name, 'email': agent.email, 'address': agent.address,'code': agent.code} for agent in agents]
        return Response(data)

    def post(self, request):
        code_agent = request.data.get('code_agent') 
        agent = Agent.objects.filter(code = code_agent).first()
        if agent:
            code_controle = generate_code()
            Send_wp(agent.phone,code_controle)
            return Response({'id':agent.id,'code': code_controle,'name':agent.name,'phone':agent.phone,'id':agent.id,'code_agent':code_agent})
        else:
            return Response({'id':0,'code': "0",'name':"agent.name",'phone':"agent.phone",'id':"agent.id",'code_agent':"code_agent"})
class CustomerCreateMarchand(APIView):
    def get(self, request):
        customers = Customer.objects.all()
        i = 0
        for c in customers:
            if c.marchand_created == False:
                result = create_marchand(c.name,"customer",c.email,"3",c.phone,"7")
                if(result):
                    c.marchand_created = True
                    i += 1
        
        return Response(i)

class CustomerApiLogin(APIView):
    def post(self, request):
        p = request.data.get('phone')
        c = Customer.objects.filter(phone = p).first()
        if c:
            code = generate_code()
            Send_wp(p,code)
            return Response({'id':c.id,'code':code})
        else:
            return Response({'id':0,'code':0})
class SendCustomerNotificationApi(APIView):
    def post(self, request):
        p = request.data.get('phone')
        message = request.data.get('msg')
        c = Customer.objects.filter(phone = p).first()
        if c:
            send_notif(c.token,"Mekka Money",message,{})
            return Response({'code':1})
        else:
            return Response({'code':0})
        
class AgentApiLogin(APIView):
    def post(self, request):
        p = request.data.get('phone')
        agent = Agent.objects.filter(phone = p).first()
        if agent:
            code = generate_code()
            Send_wp(p,code)
            return Response({'id':agent.id,'code':code})
        else:
            return Response({'id':0,'code':0})
        

        

def Send_wp(phone,code):
    url = "https://api.ultramsg.com/instance46277/messages/chat"

    payload = json.dumps({
        "token": "ucl1zdrrlnekz30x",
        "to": phone,
        "body": f"Votre code de connexion est :{code}"
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
