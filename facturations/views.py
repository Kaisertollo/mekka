from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import ListView, DetailView, View
from .models import *
from .serializers import *
import requests
import json
from django.views.decorators.csrf import csrf_exempt
import random
import string
class default(APIView):
   def get(self, request):
    return Response("hello Mekka")
class InvoiceListView(ListView):
    model = Invoice
    template_name = 'invoices/invoice_list.html'  # Replace with your template path
    context_object_name = 'invoices'

    def get(self, request, *args, **kwargs):
        invoices = self.get_queryset()
        for i in invoices:
            i.invoice_product = InvoiceProduct.objects.filter(invoice = i)
            i.calculate_total_amount()
        serializer = InvoiceSerializer(invoices, many=True)
        return JsonResponse(serializer.data, safe=False)
class InvoiceListByDate(APIView):
   def get(self, request):
        dates = Invoice.objects.values_list('date', flat=True).distinct()
        list = []
        for d in dates:
            inv = Invoice.objects.all().filter(date=d)
            for i in inv:
                i.invoice_product = InvoiceProduct.objects.filter(invoice = i)
                i.calculate_total_amount()
            s = InvoiceSerializer(inv, many=True)
            item = {"date": d.isoformat(),"invoices":s.data}
            list.append(item)
        return Response(list)
class ProductListView(ListView):
    model = Product
    template_name = 'invoices/invoice_list.html'  # Replace with your template path
    context_object_name = 'invoices'

    def get(self, request, *args, **kwargs):
        products = self.get_queryset()
        serializer = ProductSerializer(products, many=True)
        return JsonResponse(serializer.data, safe=False)
"""     @csrf_exempt
    def post(self, request):
        data = request.POST

        # Perform validation and create the invoice using the provided data

        # Example code to create a new invoice
        invoice = Invoice.objects.create(
            number=data.get('number'),
            date=data.get('date'),
            customer_id=data.get('customer_id'),
            total_amount=data.get('total_amount')
        )

        # Example code to associate products with the invoice
        product_ids = data.getlist('product_ids')
        quantities = data.getlist('quantities')
        prices = data.getlist('prices')

        for product_id, quantity, price in zip(product_ids, quantities, prices):
            InvoiceProduct.objects.create(
                invoice=invoice,
                product_id=product_id,
                quantity=quantity,
                price=price
            )

        serializer = InvoiceSerializer(invoice)
        return JsonResponse(serializer.data, status=201)

 """

class InvoiceDetailView(DetailView):
    model = Invoice
    template_name = 'invoices/invoice_detail.html'  # Replace with your template path
    context_object_name = 'invoice'

    def get(self, request, *args, **kwargs):
        invoice = self.get_object()
        print('sss')
        serializer = InvoiceSerializer(invoice)
        return JsonResponse(serializer.data)


class InvoiceCreateView(View):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        print(f"test21 {request}")
        print(f"test21 {data}")
        # Perform validation and create the invoice using the provided data

        # Example code to create a new invoice
        invoice = Invoice.objects.create(
            number=data['number'],
            date=data['date'],
            customer_id=data['customer']['id']
        )
        for item in data["invoice_product"]:
            InvoiceProduct.objects.create(
                invoice=invoice,
                product_id=item['product']["id"],
                quantity=item['quantity'],
            )

        serializer = InvoiceSerializer(invoice)
        return JsonResponse(serializer.data, status=201)


class InvoiceListView_by_customer(DetailView):
    model = Customer
    template_name = 'invoices/invoice_list.html'  # Replace with your template path
    context_object_name = 'invoices'

    def get(self, request, *args, **kwargs):
        c = self.get_object()
        #customer_id = request.GET.get('customer_id')
        invoices = Invoice.objects.filter(customer=c)

        for i in invoices:
            i.invoice_product = InvoiceProduct.objects.filter(invoice = i)
            i.calculate_total_amount()
        serializer = InvoiceSerializer(invoices, many=True)
        return JsonResponse(serializer.data, safe=False)
    
class CustomerAPI(APIView):
    def get(self, request):
        customers = Customer.objects.all()
        # Convert the customer data to JSON or any desired format
        data = [{'id':customer.id,'name': customer.name, 'email': customer.email, 'address': customer.address} for customer in customers]
        return Response(data)

    def post(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        address = request.data.get('address')
        customer = Customer.objects.create(name=name, email=email, address=address)
        return Response({'id': customer.id, 'name': customer.name, 'email': customer.email,'address': customer.address})
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
class InvoicePayAPI(APIView):
    def post(self, request):
        id_agent = request.data.get('id')
        agent = Agent.objects.filter(id = id_agent).first()
        id_invoices = request.data.get('invoices',[])
        for id_invoice in id_invoices:
            invoice = Invoice.objects.filter(id=id_invoice).first()
            invoice.payed = True
            invoice.agent = agent
            invoice.save()
        return Response({'etat':"succes"})
class CustomerApiLogin(APIView):
    def post(self, request):
        p = request.data.get('phone')
        c = Customer.objects.filter(phone = p).first()
        if c:
            code = "0000"
            Send_wp(p,code)
            return Response({'id':c.id,'code':code})
        else:
            return Response({'id':0,'code':0})
        

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
def generate_code():
    characters = string.digits
    code = ''.join(random.choice(characters) for _ in range(5))
    return code