from django.contrib import admin
from .models import *

class InvoiceProductInline(admin.TabularInline):
    model = InvoiceProduct
    extra = 1

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('number', 'date', 'customer', 'total_amount','payed')
    list_filter = ('customer',)
    search_fields = ('number', 'customer__name')
    inlines = [InvoiceProductInline]
    def total_amount(self,obj):
        return f"{obj.calculate_total_amount()} $"
    


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price')


admin.site.register(InvoiceProduct)
admin.site.register(Customer)
admin.site.register(Corporate)
admin.site.register(Agent)
