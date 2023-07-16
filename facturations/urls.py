from django.urls import path
from .views import *

app_name = 'invoices'

urlpatterns = [
    path('invoices/', InvoiceListView.as_view(), name='invoice_list'),
    path('invoicesbycustomer/<int:pk>/',InvoiceListView_by_customer.as_view(), name='invoice_list_by_customer'),
    path('invoicesbyId/<int:pk>/', InvoiceDetailView.as_view(), name='invoice_detail'),
    path('invoices/create/', InvoiceCreateView.as_view(), name='invoice_create'),
    path('api/customers/', CustomerAPI.as_view(), name='customer_api'),
    path('api/customers/login',CustomerApiLogin.as_view(), name='customer_api_login'),
]
