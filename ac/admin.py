from django.contrib import admin
from .models import Dummy,FG,TestingModel,Stage

@admin.register(Dummy)
class DummyAdmin(admin.ModelAdmin):
    list_display = ['id','user','fg_number','doc_ref_no','checklist_rev_no','customer','product_desc','pro_rev','project_name','security','in_pdf','order','para','description','remarks','position','process','timestamp','common_remarks','aps']
    

@admin.register(FG)
class FGAdmin(admin.ModelAdmin):
    list_display = ['id','user','operator_submit_user','inspector_submit_user','fg_number','doc_ref_no','checklist_rev_no','customer','customer_part_number','product_desc','pro_rev','project_name','security','work_order','starting','wo_quantity','ending','serial','in_pdf','order','para','description','remarks','common_note','position','process','submited','timestamp','operator_timestamp','inspector_timestamp','common_submit_timestamp','common_submit','common_remarks','aps','today_submit_timestamp','quantity','update','prev_submit']
    

@admin.register(TestingModel)
class TestingModelAdmin(admin.ModelAdmin):
    list_display = ['test','test_time']


@admin.register(Stage)
class StageModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'description']
