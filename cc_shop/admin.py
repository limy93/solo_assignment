from django.contrib import admin
from .models import Country, CountryMetadata, ElectricConsumption, Product, Purchase

# Customize admin for better data management
class CountryAdmin(admin.ModelAdmin):
    list_display = ('country_name', 'country_code')
    search_fields = ('country_name', 'country_code')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('description', 'price', 'country')
    list_filter = ('country',)

admin.site.register(Country, CountryAdmin)
admin.site.register(CountryMetadata)
admin.site.register(ElectricConsumption)
admin.site.register(Product, ProductAdmin)
admin.site.register(Purchase)