# Generated by Django 5.0.3 on 2024-11-05 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0004_alter_account_account_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_number',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]