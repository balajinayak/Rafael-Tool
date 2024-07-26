# Generated by Django 4.2.11 on 2024-06-09 18:17

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dummy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fg_number', models.CharField(max_length=200)),
                ('doc_ref_no', models.CharField(max_length=200)),
                ('checklist_rev_no', models.CharField(max_length=200)),
                ('customer', models.CharField(max_length=200)),
                ('product_desc', models.TextField()),
                ('product', models.CharField(max_length=200, verbose_name='ProductPartNo')),
                ('pro_rev', models.CharField(max_length=200)),
                ('project_name', models.CharField(max_length=200)),
                ('security', models.CharField(max_length=200)),
                ('marking', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('common_remarks', models.CharField(blank=True, max_length=200, null=True)),
                ('aps', models.CharField(blank=True, max_length=200, null=True)),
                ('in_pdf', models.CharField(blank=True, max_length=200, null=True)),
                ('order', models.IntegerField(blank=True, null=True)),
                ('para', models.IntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('position', models.CharField(blank=True, choices=[('operator', 'operator'), ('inspector', 'inspector'), ('both', 'both')], max_length=200, null=True)),
                ('process', models.CharField(blank=True, choices=[('common_process', 'common_process'), ('individual_process', 'individual_process')], max_length=200, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FG',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('common_submit_timestamp', models.DateTimeField(blank=True, null=True)),
                ('fg_number', models.CharField(max_length=200)),
                ('doc_ref_no', models.CharField(max_length=200)),
                ('checklist_rev_no', models.CharField(max_length=200)),
                ('customer', models.CharField(max_length=200)),
                ('customer_part_number', models.CharField(max_length=200, null=True)),
                ('product_desc', models.TextField()),
                ('product', models.CharField(max_length=200, verbose_name='ProductPartNo')),
                ('pro_rev', models.CharField(max_length=200)),
                ('project_name', models.CharField(max_length=200)),
                ('security', models.CharField(max_length=200)),
                ('common_remarks', models.CharField(blank=True, max_length=200, null=True)),
                ('aps', models.CharField(blank=True, max_length=200, null=True)),
                ('work_order', models.CharField(blank=True, max_length=200, null=True)),
                ('starting', models.CharField(blank=True, max_length=1000, null=True)),
                ('wo_quantity', models.CharField(blank=True, max_length=1000, null=True)),
                ('ending', models.CharField(blank=True, max_length=1000, null=True)),
                ('serial', models.CharField(blank=True, max_length=1000, null=True)),
                ('in_pdf', models.CharField(blank=True, max_length=200, null=True)),
                ('order', models.IntegerField(blank=True, null=True)),
                ('para', models.IntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('common_note', models.TextField(blank=True, null=True)),
                ('position', models.CharField(blank=True, choices=[('operator', 'operator'), ('inspector', 'inspector'), ('both', 'both')], max_length=200, null=True)),
                ('process', models.CharField(blank=True, choices=[('common_process', 'common_process'), ('individual_process', 'individual_process')], max_length=200, null=True)),
                ('submited', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('operator_timestamp', models.DateTimeField(blank=True, null=True)),
                ('inspector_timestamp', models.DateTimeField(blank=True, null=True)),
                ('today_submit_timestamp', models.DateTimeField(blank=True, null=True)),
                ('quantity', models.IntegerField(default=0)),
                ('update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestingModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test', models.BooleanField(default=False)),
                ('test_time', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
