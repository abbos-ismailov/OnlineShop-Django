# Generated by Django 4.2.7 on 2023-12-25 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_rename_discription_product_description_color_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brands',
            name='category',
        ),
        migrations.AddField(
            model_name='brands',
            name='category',
            field=models.ManyToManyField(blank=True, null=True, to='home.category'),
        ),
    ]