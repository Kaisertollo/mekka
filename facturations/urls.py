from django.urls import path
from .views import *
import facturations.api.invoices_api as invoice_api
import facturations.api.product_api as product_api
import facturations.api.customer_api as customer_api
import facturations.api.corporate_api as corporate_api
import facturations.api.agent_api as agent_api
app_name = 'invoices'

urlpatterns = [
    path('invoices', invoice_api.Invoices.as_view(), name='invoices'),
    path('invoice/<int:invoice_id>',invoice_api.InvoiceById.as_view(), name='invoice_by_id'),
    path('invoices_by_date', invoice_api.InvoiceListByDate.as_view(), name='invoice_by_date'),
    path('invoicesbycustomer/<int:pk>/',invoice_api.InvoiceListView_by_customer.as_view(), name='invoices_by_customer'),
    path('pay', invoice_api.InvoicePayAPI.as_view(), name='pay_api'),

    path('products',product_api.ProductAPI.as_view(), name='products'),
    path('product/<int:product_id>',product_api.ProductById.as_view(), name='product_by_id'),

    path('customers', customer_api.CustomerAPI.as_view(), name='customers'),
    path('customer/<int:customer_id>',customer_api.CustomerById.as_view(), name='customer_by_id'),
    path('customers/login',customer_api.CustomerApiLogin.as_view(), name='customer_api_login'),
    path('customers/create_pwd',customer_api.CustomerCreatePassword.as_view(), name='customer_api_create_pwd'),
    path('customers/login_pwd',customer_api.CustomerLoginPassword.as_view(), name='customer_api_login_pwd'),
    path('send_customer_notification',SendCustomerNotificationApi.as_view(), name='customer_send_notification'),
    path('customer/token',customer_api.CustomerTokenAPI.as_view(), name='customer_api_token'),

    path('corporates', corporate_api.CorporateAPI.as_view(), name='corporates'),
    path('corporate/<int:corporate_id>',corporate_api.CorporateById.as_view(), name='corporate_by_id'),
    path('corporate/login',corporate_api.CorporateApiLogin.as_view(), name='corporate_api_login'),
    
    path('agents', agent_api.AgentAPI.as_view(), name='agents'),
    path('agent/<int:agent_id>',agent_api.AgentById.as_view(), name='agent_by_id'),
    path('agent/check', AgentAPI.as_view(), name='agent_check_api'),


    path('customer/marchand/create', CustomerCreateMarchand.as_view(), name='customer_marchand_create'),
    path('agent/login',AgentApiLogin.as_view(), name='agent_api_login'),
    path('agent/token',agent_api.AgentTokenAPI.as_view(), name='agent_api_token'),
    
]
