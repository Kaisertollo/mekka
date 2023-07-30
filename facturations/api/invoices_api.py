from facturations.models import *
from facturations.serializers import InvoiceSerializer
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, View
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from facturations.utils import generate_code,Send_wp
import json
class Invoices(APIView):
    def get(self, request):
        invoices = Invoice.objects.all()
        for i in invoices:
            i.invoice_product = InvoiceProduct.objects.filter(invoice = i)
            i.calculate_total_amount()
        serializer = InvoiceSerializer(invoices, many=True)
        return JsonResponse(serializer.data, safe=False)
    def post(self,request):
        data = request.data
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
        invoice.invoice_product = InvoiceProduct.objects.filter(invoice = invoice)
        serializer = InvoiceSerializer(invoice)
        return JsonResponse(serializer.data, status=201)
class InvoiceById(APIView):
    def get(self, request,invoice_id):
        invoice = Invoice.objects.get(id = invoice_id)
        invoice.invoice_product = InvoiceProduct.objects.filter(invoice = invoice)
        invoice.calculate_total_amount()
        serializer = InvoiceSerializer(invoice)
        return JsonResponse(serializer.data, safe=False)
    def put(self, request, invoice_id):
        try:
            invoice = Invoice.objects.get(id=invoice_id)
        except Invoice.DoesNotExist:
            return JsonResponse({'error': 'Invoice not found'}, status=status.HTTP_404_NOT_FOUND)

        invoice = Invoice.objects.get(id=invoice_id)
        data = request.data
        customer = Customer.objects.get(id = data['customer_id'])
        corporate = Corporate.objects.get(id = data['corporate'])
        invoice.customer = customer
        invoice.corporate = corporate
        invoice.number = data['number']
        invoice.date = data['date']
        invoice.payed = data['payed']
        list = []
        for item in data["invoice_product"]:
            ip = InvoiceProduct.objects.get(id = item['id'])
            product = Product.objects.get(id = item['product_id'])
            ip.product = product
            ip.quantity = item['product_id']
            list.append(ip)
        invoice.invoice_product = list
        invoice.calculate_total_amount()
        invoice.save()
        return Response(InvoiceSerializer(invoice).data)
    def delete(self, request, invoice_id):
        try:
            invoice = Invoice.objects.get(id=invoice_id)
            invoice.delete()
            return Response({'status': 'deleted'})
        except Invoice.DoesNotExist:
            return JsonResponse({'error': 'Invoice not found'}, status=status.HTTP_404_NOT_FOUND)

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