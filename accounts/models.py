from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    position_options = (
        ('operator','operator'),
        ('inspector','inspector'),
    )
    position = models.CharField(max_length=200, choices=position_options)
    is_supervisor = models.BooleanField(default=False)
    is_submit = models.BooleanField(default=False)
    is_submit_time = models.DateTimeField(null=True,blank=True)

#    class Meta:
#        app_label = 'accounts'
#
#CustomUser.groups.field.remote_field.related_name = 'custom_user_groups'
#CustomUser.user_permissions.field.remote_field.related_name = 'custom_user_permissions'