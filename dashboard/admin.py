from django.contrib import admin
from .models import *

@admin.register(SIPlan)
class SIPlanAdmin(admin.ModelAdmin):
    list_display=['id','date','project','product','cdlm_part_number','description','po','line','offering_quantity','total_quantity','si_level','mrb_numbers','remarks']



@admin.register(AllSIPlan)
class AllSIPlanAdmin(admin.ModelAdmin):
    list_display=['id','date','project','product','cdlm_part_number','description','po','line','offering_quantity','total_quantity','si_level','mrb_numbers','remarks']



@admin.register(SerialNumber)
class SerialNumberAdmin(admin.ModelAdmin):
    list_display=['id','project','po_number','ncr_number','date','customer_part_number','cyient_part_number','quantity','serial_number']



@admin.register(AllSerial)
class AllSerialAdmin(admin.ModelAdmin):
    list_display=['id','serial_number','project','po_number','ncr_number','date','customer_part_number','cyient_part_number','quantity']

@admin.register(Ncrdump)
class NcrdumpAdmin(admin.ModelAdmin):
    list_display=['id','project','date','ncrno','ccaapp','infgpn','ponum','ncrdetails','proslno','ncrqty','ncrstatus','approvalstatus','remarks','qa','poqty','shipqty','openqty','timestamp']



@admin.register(Mapping)
class MappingAdmin(admin.ModelAdmin):
    list_display=['id', 'bare_pcb_serial_number', 'cca_serial_number','work_order_number','fg_part_number','customer']



@admin.register(NCRTracker)
class NCRTrackerAdmin(admin.ModelAdmin):
    list_display=[
    'project',
    'serial_number',
    'ncr_date',
    'ncr_number',
    'customer_part_number',
    'internal_fg_partnumber',
    'po_number',
    'details',
    'ncr_quantity',
    'remaining',
    'consumed',
    'add_quantity',
    'ncr_status',
    'approval_status',
    'approval_Date',
    'document',
    'timestamp',
    'site',
    'customer',
    'product_description',
    'product_part_number',
    'issue_reported_stage',
    'po_details',
    'product_rev',
    'cyient_fg_number',
    'issued_by',
    'issued_to',
    'lot',
    'lot_and_defect_status',
    'image1',
    'image2',
    'circuit_reference_or_ref_designator',
    'number_of_defects',
    'containment_action',
    'containment_resp',
    'containment_date',
    'root_cause_analysis',
    'why1',
    'why1_man',
    'why1_method',
    'why1_material',
    'why1_machine',
    'why2',
    'why2_man',
    'why2_method',
    'why2_material',
    'why2_machine',
    'why3',
    'why3_man',
    'why3_method',
    'why3_material',
    'why3_machine',
    'why4',
    'why4_man',
    'why4_method',
    'why4_material',
    'why4_machine',
    'why5',
    'why5_man',
    'why5_method',
    'why5_material',
    'why5_machine',
    'corrective_action',
    'corrective_resp',
    'corrective_date',
    'preventive_action',
    'preventive_resp',
    'preventive_date',
    'wo_no',
    'batch_no',
    'verification_details',
    'verification_status',
    'verification_resp',
    'varifiction_date',
]


@admin.register(POTracker)
class POTrackerAdmin(admin.ModelAdmin):
    list_display=['id','project','customer','ship_to','rafael_part_number','cyient_part_number','description',
        'po_number','poline','quantity','consumed','remaining','add_quantity','timestamp'
        ]


@admin.register(DefectiveLibrary)
class DefectiveLibraryAdmin(admin.ModelAdmin):
    list_display=['id','customer','project','product_part_number','brief_defect_description','customer_part_number','product_rev','product_description','complaint_description','source_of_complaint','quantity_affected','original_date','reported_on','defect_image_available','defect_image','root_cause','ca_pa','defect_cause']



@admin.register(SIShipped)
class SIShippedAdmin(admin.ModelAdmin):
    list_display=['sl_no','invoice_date','customer_part_number','cdlm_part_number','invoice_no','po_number',
    'customer','serial_number','quantity','remarks'
    ]



@admin.register(AllSIShipped)
class AllSIShippedAdmin(admin.ModelAdmin):
    list_display=['sl_no','invoice_date','customer_part_number','cdlm_part_number','invoice_no','po_number',
    'customer','serial_number','quantity','remarks'
    ]


@admin.register(DlCustomer)
class DlCustomerAdmin(admin.ModelAdmin):
    list_display=['title']


@admin.register(DlProject)
class DlProjectAdminAdmin(admin.ModelAdmin):
    list_display=['title']


@admin.register(DlProductPartNumber)
class DlProductPartNumberAdmin(admin.ModelAdmin):
    list_display=['title']


@admin.register(DlBriefDefectDescription)
class DlBriefDefectDescriptionAdmin(admin.ModelAdmin):
    list_display=['title']


@admin.register(DlCustomerPartNumber)
class DlCustomerPartNumberAdmin(admin.ModelAdmin):
    list_display=['title']


@admin.register(DlProductDescription)
class DlProductDescriptionAdmin(admin.ModelAdmin):
    list_display=['title']


@admin.register(DlComplaintDescription)
class DlComplaintDescriptionAdmin(admin.ModelAdmin):
    list_display=['title']


@admin.register(DlSourceofComplaint)
class DlSourceofComplaintAdmin(admin.ModelAdmin):
    list_display=['title']

@admin.register(DlMappingCustomer)
class DlMappingCustomerAdmin(admin.ModelAdmin):
    list_display=['title']




