from django.urls import path
from .views import InvoiceListView, InvoiceDetailView, InvoiceCreateView

app_name = 'invoices'

urlpatterns = [
    path('invoices/', InvoiceListView.as_view(), name='invoice_list'),
    path('invoices/<int:pk>/', InvoiceDetailView.as_view(), name='invoice_detail'),
    path('invoices/create/', InvoiceCreateView.as_view(), name='invoice_create'),
]
