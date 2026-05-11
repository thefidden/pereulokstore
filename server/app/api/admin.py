from io import BytesIO

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from io import BytesIO
from django.core.files.base import ContentFile
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.utils import timezone
from django.conf import settings
from .models import ProductReport

from import_export.admin import ImportExportModelAdmin

from .models import Product, ProductImage, Cart, Order, OrderProduct, Tag, ProductTag, ProductReport


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image',)
    readonly_fields = ()


class ProductTagInline(admin.TabularInline):
    model = ProductTag
    extra = 1
    fields = ('tag', 'priority', 'added_at')
    readonly_fields = ('added_at',)


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ('name', 'type', 'price', 'creation_date', 'link')
    list_display_links = ('name',)
    list_filter = ('type', 'price', 'creation_date')
    search_fields = ('name', 'description')
    inlines = [ProductImageInline, ProductTagInline]
    date_hierarchy = 'creation_date'
    actions = ['generate_pdf_report']
    readonly_fields = ['slug', 'source_url']

    @admin.display()
    def link(self, obj: Product):
        return format_html(
            '<a href="{}" target="_blank">{}</a>',
            obj.source_url,
            obj.source_url
        )

    link.short_description = 'Ссылка на товар'

    @admin.action(description = 'Сформировать отчет по товарам')
    def generate_pdf_report(self, request, queryset):
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize = A4)
        width, height = A4

        pdf.setTitle('Отчет по товарам')

        try:
            registerFont(TTFont(settings.CYRILLIC_FONT_NAME, settings.CYRILLIC_FONT_PATH))
        except:
            pass

        # Заголовок
        pdf.setFont(settings.CYRILLIC_FONT_NAME, 16)
        pdf.drawString(40, height - 40, 'Отчет по товарам')

        # Таблица
        pdf.setFont(settings.CYRILLIC_FONT_NAME, 10)
        y = height - 70

        headers = ['Название', 'Категория', 'Цена', 'Дата создания']
        pdf.drawString(40, y, headers[0])
        pdf.drawString(220, y, headers[1])
        pdf.drawString(340, y, headers[2])
        pdf.drawString(420, y, headers[3])
        y -= 20

        for product in queryset.order_by('name', 'creation_date'):
            if y < 40:
                pdf.showPage()
                pdf.setFont('Helvetica', 10)
                y = height - 40

            pdf.drawString(40, y, str(product.name)[:30])
            pdf.drawString(220, y, str(product.get_type_display())[:18])
            pdf.drawString(340, y, str(product.price))
            pdf.drawString(420, y, product.creation_date.strftime('%Y-%m-%d %H:%M'))
            y -= 18

        pdf.save()

        report = ProductReport.objects.create(created_by = request.user)
        report.file.save(
            f'product-report-{timezone.now():%Y%m%d-%H%M%S}.pdf',
            ContentFile(buffer.getvalue()),
            save = True
        )

        self.message_user(request, f'Отчет создан: {report.file.name}')


@admin.register(Tag)
class TagAdmin(ImportExportModelAdmin):
    list_display = ('name', 'slug')
    list_display_links = ('name',)
    search_fields = ('name', 'slug')
    readonly_fields = ('slug',)  # Slug генерируется автоматически


@admin.register(Cart)
class CartAdmin(ImportExportModelAdmin):
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
class OrderAdmin(ImportExportModelAdmin):
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
class OrderProductAdmin(ImportExportModelAdmin):
    list_display = ('order', 'product', 'price', 'amount')
    list_display_links = ('order', 'product')
    list_filter = ('order', 'product')
    search_fields = ('order__id', 'product__name')
    raw_id_fields = ('order', 'product')


admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(ImportExportModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    filter_horizontal = ('groups', 'user_permissions')


@admin.register(ProductReport)
class ProductReportAdmin(ImportExportModelAdmin):
    list_display = ('file', 'created_at', 'created_by')
    list_filter = ('created_at', 'created_by')
    raw_id_fields = ('created_by',)
    readonly_fields = ('file', 'created_at', 'created_by')
