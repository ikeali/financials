# Generated by Django 5.0.3 on 2024-11-05 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0005_alter_account_account_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='bank_name',
            field=models.CharField(max_length=100),
        ),
    ]
