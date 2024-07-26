# Generated by Django 4.2.11 on 2024-06-09 18:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ac', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fg',
            name='common_submit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='commonSubmit', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='fg',
            name='inspector_submit_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inspector_submited_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='fg',
            name='operator_submit_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='operator_submited_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='fg',
            name='today_submit_user',
            field=models.ManyToManyField(related_name='today_submited_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='fg',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dummy',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
