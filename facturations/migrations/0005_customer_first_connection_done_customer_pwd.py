# Generated by Django 4.2.3 on 2023-09-08 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturations', '0004_agent_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='first_connection_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customer',
            name='pwd',
            field=models.CharField(default='', max_length=200),
        ),
    ]