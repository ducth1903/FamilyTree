# Generated by Django 3.0.7 on 2020-07-02 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tree', '0005_auto_20200701_2249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='couple',
            name='husband_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='couple',
            name='wife_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]