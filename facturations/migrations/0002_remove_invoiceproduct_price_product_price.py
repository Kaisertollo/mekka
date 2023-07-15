# Generated by Django 4.2.3 on 2023-07-14 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturations', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoiceproduct',
            name='price',
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]
