# Generated by Django 3.0.7 on 2020-07-02 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tree', '0004_auto_20200701_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='couple',
            name='husband_bornPlace',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='couple',
            name='husband_deceasedDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='couple',
            name='husband_dob',
            field=models.DateField(blank=True, null=True, verbose_name=['%m/%d/%Y']),
        ),
        migrations.AlterField(
            model_name='couple',
            name='husband_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='couple',
            name='husband_occupation',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='couple',
            name='parent_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='couple',
            name='wife_bornPlace',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='couple',
            name='wife_deceasedDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='couple',
            name='wife_dob',
            field=models.DateField(blank=True, null=True, verbose_name=['%m/%d/%Y']),
        ),
        migrations.AlterField(
            model_name='couple',
            name='wife_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='couple',
            name='wife_occupation',
            field=models.TextField(blank=True, null=True),
        ),
    ]
