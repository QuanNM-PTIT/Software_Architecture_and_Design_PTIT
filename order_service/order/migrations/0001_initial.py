# Generated by Django 4.1.13 on 2024-05-21 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('order_item_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField()),
                ('product_id', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=10)),
                ('quantity', models.IntegerField()),
                ('status', models.IntegerField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('payment_id', models.IntegerField(null=True)),
                ('shipment_id', models.IntegerField(null=True)),
            ],
        ),
    ]
