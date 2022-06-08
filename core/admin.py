from django.contrib import admin

# Register your models here.
from .models import Product, OrderProduct, Order, Review


admin.site.register(Product)
admin.site.register(OrderProduct)
admin.site.register(Order)
admin.site.register(Review)