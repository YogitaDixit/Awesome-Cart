from django.contrib import admin
from .models import Product, Contact, Orders, OrderUpdate, CartItem, Address

admin.site.register(Product)
admin.site.register(Contact)

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):

    list_display = (
        "order_id",
        "name",
        "email",
        "status",
        "order_date",
    )

    list_filter = (
        "status",
        "order_date",
    )

    search_fields = (
        "order_id",
        "name",
        "email",
    )

    readonly_fields = (
        "order_id",
        "user",
        "address",
        "items_json",
        "name",
        "email",
        "city",
        "state",
        "zip_code",
        "phone",
        "order_date",
    )

    fields = (
        "order_id",
        "user",
        "name",
        "email",
        "address",
        "city",
        "state",
        "zip_code",
        "phone",
        "items_json",
        "order_date",
        "status",
    )
admin.site.register(OrderUpdate)
admin.site.register(CartItem)
admin.site.register(Address)