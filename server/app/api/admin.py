from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html

from .models import Product, ProductImage, Cart, Order, OrderProduct, AuthenticationToken, AuthenticationRequest, \
    UserImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image',)
    readonly_fields = ()


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'price', 'creation_date', 'link')
    list_display_links = ('name',)
    list_filter = ('type',)
    search_fields = ('name', 'description')
    inlines = [ProductImageInline]
    date_hierarchy = 'creation_date'

    @admin.display()
    def link(self, obj: Product):
        return format_html(
            '<a href="{}" target="_blank">Перейти к товару на сайте</a>',
            f'/products/{obj.id}'
        )

    link.short_description = 'Ссылка на товар'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'amount', 'creation_date')
    list_display_links = ('user', 'product')
    list_filter = ('user', 'product')
    search_fields = ('user__username', 'product__name')
    raw_id_fields = ('user', 'product')


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0
    raw_id_fields = ('product',)
    fields = ('product', 'price', 'amount')
    readonly_fields = ('product', 'price', 'amount')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'price', 'datetime', 'products_count')
    list_display_links = ('id', 'user')
    list_filter = ('status', 'datetime')
    search_fields = ('user__username', 'user__first_name', 'products__product__name')
    date_hierarchy = 'datetime'
    inlines = [OrderProductInline]
    raw_id_fields = ('user',)
    readonly_fields = ('price', 'user', 'datetime')

    @admin.display(description = 'Количество позиций')
    def products_count(self, obj):
        return obj.products.count()

    products_count.short_description = 'Количество позиций'


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'price', 'amount')
    list_display_links = ('order', 'product')
    list_filter = ('order', 'product')
    search_fields = ('order__id', 'product__name')
    raw_id_fields = ('order', 'product')


@admin.register(AuthenticationToken)
class AuthenticationTokenAdmin(admin.ModelAdmin):
    list_display = ('id',)
    search_fields = ('id',)


@admin.register(AuthenticationRequest)
class AuthenticationRequestAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'telegram_username', 'telegram_name')
    list_display_links = ('telegram_id',)
    search_fields = ('telegram_id', 'telegram_username', 'telegram_name')
    readonly_fields = ('token',)


@admin.register(UserImage)
class UserImageAdmin(admin.ModelAdmin):
    list_display = ('user', 'image')
    list_display_links = ('user',)
    search_fields = ('user__username',)
    raw_id_fields = ('user',)


admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    filter_horizontal = ('groups', 'user_permissions')
