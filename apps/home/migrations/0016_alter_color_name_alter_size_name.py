# Generated by Django 4.2.7 on 2023-12-19 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_remove_product_stars_percent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color',
            name='name',
            field=models.CharField(max_length=120),
        ),
        migrations.AlterField(
            model_name='size',
            name='name',
            field=models.CharField(max_length=120),
        ),
    ]
