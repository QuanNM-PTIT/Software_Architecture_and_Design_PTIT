# Generated by Django 4.1.13 on 2024-05-22 03:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_model', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_model.account', unique=True),
        ),
    ]
