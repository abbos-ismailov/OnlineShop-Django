# Generated by Django 4.2.7 on 2023-12-10 06:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_alter_bannerdiscount_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreview',
            name='stars',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
