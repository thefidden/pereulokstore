import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


def fill_product_slug_and_source_url(apps, schema_editor):
    Product = apps.get_model('api', 'Product')

    for product in Product.objects.all().only('id', 'slug', 'source_url'):
        slug = product.slug or f'product-{product.id.hex}'
        source_url = product.source_url or f'https://pereulokstore.local/products/{product.id}/'
        Product.objects.filter(pk=product.pk).update(slug=slug, source_url=source_url)


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0016_product_source_url'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, max_length=50, null=True, unique=True, verbose_name='Slug'),
        ),
        migrations.CreateModel(
            name='ProductReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='reports', verbose_name='PDF-отчет')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_reports', to=settings.AUTH_USER_MODEL, verbose_name='Создано пользователем')),
            ],
            options={
                'verbose_name': 'Отчет по товарам',
                'verbose_name_plural': 'Отчеты по товарам',
                'ordering': ['-created_at'],
            },
        ),
        migrations.RunPython(fill_product_slug_and_source_url, migrations.RunPython.noop),
    ]
