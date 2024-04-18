from django.contrib import admin
from .models import Product, Country, ElectricConsumption, CountryMetadata, Purchase

# Customize admin for better data management, if needed
class CountryAdmin(admin.ModelAdmin):
    list_display = ('country_name', 'country_code')
    search_fields = ('country_name', 'country_code')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('description', 'price', 'country')
    list_filter = ('country',)

# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(ElectricConsumption)
admin.site.register(CountryMetadata)
admin.site.register(Purchase)