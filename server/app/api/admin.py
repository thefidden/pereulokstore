from django.contrib import admin

from .models import Product, ProductImage, Cart, Order, OrderProduct


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]


class OrderProductAdmin(admin.StackedInline):
    model = OrderProduct
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductAdmin]


admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(Order, OrderAdmin)
