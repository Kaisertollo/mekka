from django.urls import path
from .views import *

app_name = 'invoices'

urlpatterns = [
    path('invoices', InvoiceListView.as_view(), name='invoice_list'),
    path('products', ProductListView.as_view(), name='product_list'),
    path('invoicesbycustomer/<int:pk>/',InvoiceListView_by_customer.as_view(), name='invoice_list_by_customer'),
    path('invoicesbyId/<int:pk>', InvoiceDetailView.as_view(), name='invoice_detail'),
    path('invoices/create', InvoiceCreateView.as_view(), name='invoice_create'),
    path('customers', CustomerAPI.as_view(), name='customer_api'),
    path('customers/login',CustomerApiLogin.as_view(), name='customer_api_login'),
    path('corporate/login',CorporateApiLogin.as_view(), name='corporate_api_login'),
    path('agent/check', AgentAPI.as_view(), name='agent_check_api'),
    path('pay', InvoicePayAPI.as_view(), name='pay_api'),
]
