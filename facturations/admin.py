from django.contrib import admin
from .models import Invoice, Product, InvoiceProduct,Customer


class InvoiceProductInline(admin.TabularInline):
    model = InvoiceProduct
    extra = 1


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('number', 'date', 'customer', 'total_amount')
    list_filter = ('customer',)
    search_fields = ('number', 'customer__name')
    inlines = [InvoiceProductInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(InvoiceProduct)
admin.site.register(Customer)
