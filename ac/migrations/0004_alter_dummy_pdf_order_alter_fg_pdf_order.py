# Generated by Django 4.2.11 on 2024-09-26 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ac', '0003_remove_fg_prev_submit_serial_dummy_pdf_order_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dummy',
            name='pdf_order',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='fg',
            name='pdf_order',
            field=models.CharField(blank=True, null=True),
        ),
    ]
