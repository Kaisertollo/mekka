# Generated by Django 4.2.3 on 2023-08-13 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturations', '0003_corporate_marchand_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='token',
            field=models.CharField(default=0, max_length=250),
            preserve_default=False,
        ),
    ]