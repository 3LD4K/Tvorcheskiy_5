from django.contrib import admin
from .models import Customer, Product, Installment

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Installment)
