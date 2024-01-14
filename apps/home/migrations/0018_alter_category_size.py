# Generated by Django 4.2.7 on 2023-12-19 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_category_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='size',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='size_category', to='home.size'),
        ),
    ]