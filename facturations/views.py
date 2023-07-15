from django.http import JsonResponse
from django.views.generic import ListView, DetailView, View
from .models import *
from .serializers import *
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
class InvoiceListView(ListView):
    model = Invoice
    template_name = 'invoices/invoice_list.html'  # Replace with your template path
    context_object_name = 'invoices'

    def get(self, request, *args, **kwargs):
        customer_id = request.GET.get('customer_id')
        if customer_id:
            invoices = self.get_queryset().filter(customer_id=customer_id)
        else:
            invoices = self.get_queryset()
            for i in invoices:
                i.invoice_product = InvoiceProduct.objects.filter(invoice = i)
                i.calculate_total_amount()

        serializer = InvoiceSerializer(invoices, many=True)
        return JsonResponse(serializer.data, safe=False)

from django.views.decorators.csrf import csrf_exempt
class InvoiceDetailView(DetailView):
    model = Invoice
    template_name = 'invoices/invoice_detail.html'  # Replace with your template path
    context_object_name = 'invoice'

    def get(self, request, *args, **kwargs):
        invoice = self.get_object()
        serializer = InvoiceSerializer(invoice)
        return JsonResponse(serializer.data)

from django.views.decorators.csrf import csrf_exempt
class InvoiceCreateView(View):

    def post(self, request, *args, **kwargs):
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
