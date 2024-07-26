from django.db import models
from accounts.models import CustomUser
from ckeditor.fields import RichTextField
import re



class Dummy(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    fg_number = models.CharField(max_length=200)
    doc_ref_no = models.CharField(max_length=200)
    checklist_rev_no = models.CharField(max_length=200)
    customer = models.CharField(max_length=200)
    product_desc = models.TextField()
    product = models.CharField(max_length=200, verbose_name='ProductPartNo')
    pro_rev = models.CharField(max_length=200)
    project_name = models.CharField(max_length=200)
    security =  models.CharField(max_length=200)
    marking = RichTextField(null=True, blank=True)
    common_remarks = models.CharField(max_length=200, null=True, blank=True)
    aps = models.CharField(max_length=200, null=True, blank=True)
    in_pdf = models.CharField(max_length=200, null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)
    para = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    position_options = (
        ('operator','operator'),
        ('inspector','inspector'),
        ('both','both'),
    )
    process_options = (
        ('common_process','common_process'),
        ('individual_process','individual_process'),
    )
    position = models.CharField(max_length=200, choices=position_options, null=True, blank=True)
    process = models.CharField(max_length=200, choices=process_options, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.fg_number


class FG(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    common_submit = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='commonSubmit')
    common_submit_timestamp = models.DateTimeField(null=True, blank=True)
    fg_number = models.CharField(max_length=200)
    doc_ref_no = models.CharField(max_length=200)
    checklist_rev_no = models.CharField(max_length=200)
    customer = models.CharField(max_length=200)
    customer_part_number = models.CharField(max_length=200, null=True)
    product_desc = models.TextField()
    product = models.CharField(max_length=200, verbose_name='ProductPartNo')
    pro_rev = models.CharField(max_length=200)
    project_name = models.CharField(max_length=200)
    security =  models.CharField(max_length=200)
    common_remarks = models.CharField(max_length=200, null=True, blank=True)
    aps = models.CharField(max_length=200, null=True, blank=True)
    work_order = models.CharField(max_length=200, null=True, blank=True)
    starting = models.CharField(max_length=1000, null=True, blank=True)
    wo_quantity = models.CharField(max_length=1000, null=True, blank=True)
    ending = models.CharField(max_length=1000, null=True, blank=True)
    serial = models.CharField(max_length=1000, null=True, blank=True)
    in_pdf = models.CharField(max_length=200, null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)
    para = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    common_note = models.TextField(null=True, blank=True)
    position_options = (
        ('operator','operator'),
        ('inspector','inspector'),
        ('both','both'),
    )
    process_options = (
        ('common_process','common_process'),
        ('individual_process','individual_process'),
    )
    position = models.CharField(max_length=200, choices=position_options, null=True, blank=True)
    process = models.CharField(max_length=200, choices=process_options, null=True, blank=True)
    submited = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    operator_submit_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="operator_submited_user")
    inspector_submit_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="inspector_submited_user")
    operator_timestamp = models.DateTimeField(null=True, blank=True)
    inspector_timestamp = models.DateTimeField(null=True, blank=True)
    today_submit_user = models.ManyToManyField(CustomUser, related_name="today_submited_user")
    today_submit_timestamp = models.DateTimeField(null=True, blank=True)
    quantity = models.IntegerField(default=0)
    update = models.DateTimeField(auto_now=True)
    prev_submit = models.BooleanField(default=False)


    def __str__(self):
        return self.fg_number

    def get_remarks_number(self):
        text = self.remarks
        parts = text.split(" ", 1)
        before_space = parts[0]
        after_space = parts[1] if len(parts) > 1 else ""
        if before_space.endswith('.'):
            before_space = before_space[:-1]
        return before_space


    def get_remarks_text(self):
        text = self.remarks
        parts = text.split(" ", 1)
        before_space = parts[0]
        after_space = parts[1] if len(parts) > 1 else ""
        if before_space.endswith('.'):
            before_space = before_space[:-1]
        return after_space

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=FG)
def user_saved(sender, instance, created, **kwargs):
    if created:
        if instance.order == 1 and instance.process == "common_process":
            instance.prev_submit = True
            instance.save(update_fields=['prev_submit'])




class TestingModel(models.Model):
    test = models.BooleanField(default=False)
    test_time = models.DateTimeField(null=True, blank=True)




class Stage(models.Model):
    description = models.CharField(null=True, blank=True)

    def __str__(self):
        return self.description