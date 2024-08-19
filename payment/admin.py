from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

# create an OrderItem inline
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

# extend our order model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_ordered"]
    inlines = [OrderItemInline]

# unregister order model
admin.site.unregister(Order)

# re-register our Order and OrderAdmin
admin.site.register(Order, OrderAdmin)