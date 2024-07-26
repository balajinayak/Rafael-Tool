from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver



class SIPlan(models.Model):
    date = models.DateField(verbose_name="Date")
    project = models.CharField(max_length=200, verbose_name="Project")
    product = models.CharField(max_length=200, verbose_name="Product")
    cdlm_part_number = models.CharField(max_length=200, verbose_name="CDLM P/N")
    description = models.CharField(max_length=2000, verbose_name="Product Description")
    po = models.TextField(null=True , blank=True,max_length=200, verbose_name="PO")
    line = models.CharField(null=True , blank=True,max_length=200, verbose_name="Line")
    offering_quantity = models.IntegerField(null=True , blank=True,verbose_name="Offering Qty")
    total_quantity = models.IntegerField(verbose_name="Total Qty")
    si_level = models.CharField(max_length=200, verbose_name="SI Level")
    mrb_numbers = models.TextField( verbose_name="MRB Numbers")
    remarks = models.TextField( verbose_name="Remarks")


    def __str__(self):
        return self.product

    def save(self, *args, **kwargs):
        if self.po:
            split_values = [value.strip() for value in self.po.split(',')]
            self.po = ','.join(split_values)
        if self.mrb_numbers:
            split_values = [value.strip() for value in self.mrb_numbers.split(',')]
            self.mrb_numbers = ','.join(split_values)
        if self.remarks:
            split_values = [value.strip() for value in self.remarks.split(',')]
            self.remarks = ','.join(split_values)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['date']



@receiver(post_save, sender=SIPlan)
def si_plan_post_save(sender, instance, created, **kwargs):
    if created:
        AllSIPlan.objects.create(
            date=instance.date,
            project=instance.project,
            product=instance.product,
            cdlm_part_number=instance.cdlm_part_number,
            description=instance.description,
            po=instance.po,
            line=instance.line,
            offering_quantity=instance.offering_quantity,
            total_quantity=instance.total_quantity,
            si_level=instance.si_level,
            mrb_numbers=instance.mrb_numbers,
            remarks=instance.remarks,
        )



class AllSIPlan(models.Model):

    date = models.DateField(verbose_name="Date")
    project = models.CharField(max_length=200, verbose_name="Project")
    product = models.CharField(max_length=200, verbose_name="Product")
    cdlm_part_number = models.CharField(max_length=200, verbose_name="CDLM P/N")
    description = models.CharField(max_length=2000, verbose_name="Product Description")
    po = models.CharField(max_length=200, verbose_name="PO")
    line = models.CharField(max_length=200, verbose_name="Line")
    offering_quantity = models.IntegerField(verbose_name="Offering Qty")
    total_quantity = models.IntegerField(verbose_name="Total Qty")
    si_level = models.CharField(max_length=200, verbose_name="SI Level")
    mrb_numbers = models.TextField(verbose_name="MRB Numbers")
    remarks = models.TextField( verbose_name="Remarks")

    def __str__(self):
        return self.product


    class Meta:
        ordering = ['date']



class SerialNumber(models.Model):
    project = models.CharField(max_length=200, verbose_name="Project")
    po_number = models.CharField(max_length=200, verbose_name="PO Number")
    ncr_number = models.CharField(max_length=200, verbose_name="NCR Number")
    date = models.DateField(verbose_name="Date")
    customer_part_number = models.CharField(max_length=200, verbose_name="Customer Part Number")
    cyient_part_number = models.CharField(max_length=200, verbose_name="Cyient Part Number")
    quantity = models.IntegerField(verbose_name="Quantity")
    serial_number = models.TextField(verbose_name="Serial Number")

    def __str__(self):
        return self.project


    class Meta:
        ordering = ['date']


    def save(self, *args, **kwargs):
        ser_num = self.serial_number.split()
        for ser in ser_num:
            AllSerial.objects.create(serial_number=ser,project=self.project,po_number=self.po_number,ncr_number=self.ncr_number,date=self.date,customer_part_number=self.customer_part_number,cyient_part_number=self.cyient_part_number,quantity=self.quantity)
        super().save(*args, **kwargs)

    
class AllSerial(models.Model):
    serial_number = models.CharField(max_length=200, verbose_name="Serial Number")
    project = models.CharField(max_length=200, verbose_name="Project")
    po_number = models.CharField(max_length=200, verbose_name="PO Number")
    ncr_number = models.CharField(max_length=200, verbose_name="NCR Number")
    date = models.DateField(verbose_name="Date")
    customer_part_number = models.CharField(max_length=200, verbose_name="Customer Part Number")
    cyient_part_number = models.CharField(max_length=200, verbose_name="Cyient Part Number")
    quantity = models.IntegerField(verbose_name="Quantity")

    def __str__(self):
        return self.project



class DlMappingCustomer(models.Model):
    title = models.CharField(max_length=250,null=True,blank=True)

    def __str__(self):
        return self.title

class Mapping(models.Model):
    bare_pcb_serial_number = models.CharField(max_length=200,null=True,blank=True)
    cca_serial_number = models.CharField(max_length=200,null=True,blank=True)
    work_order_number = models.CharField(max_length=200,null=True,blank=True)
    fg_part_number = models.CharField(max_length=200,null=True,blank=True)
    customer = models.ForeignKey(DlMappingCustomer ,verbose_name="Customer",on_delete=models.PROTECT)
    date=models.DateField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return self.bare_pcb_serial_number



class NCRTracker(models.Model):

    status = (
        ('Open', 'Open'),
        ('Closed', 'Closed'),
        (' Under Observation', ' Under Observation'),
    )

    ncr_status_choice = (
        ('In_Progress', 'In_progress'),
        ('Closed', 'Closed')

    )

    ncr_approval_status = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
    )

    project = models.CharField(max_length=200, verbose_name="Project")
    serial_number = models.CharField(max_length=200, verbose_name="Serial Number")
    ncr_date = models.DateField(verbose_name="NCR Date")
    ncr_number = models.CharField(max_length=200, verbose_name="NCR Number")
    customer_part_number = models.CharField(max_length=200, verbose_name="Customer Part No")
    internal_fg_partnumber = models.CharField(max_length=200, verbose_name="Internal FG Part No")
    po_number = models.CharField(max_length=200, verbose_name="PO Number")
    details = models.TextField(verbose_name="Details")
    ncr_quantity = models.IntegerField(default=0, verbose_name="NCR Quantity")
    remaining = models.IntegerField(default=0, verbose_name="Remaining")
    consumed = models.IntegerField(default=0, verbose_name="Consumed")
    add_quantity = models.IntegerField(default=0, verbose_name="Added Quantity")
    ncr_status = models.CharField(max_length=200,  choices=ncr_status_choice, verbose_name="NCR Status")
    approval_status = models.CharField(max_length=200, choices=ncr_approval_status, verbose_name="Approval Status")
    approval_Date = models.DateField(verbose_name="Approval Date")
    document = models.FileField(blank=True, null=True, upload_to="ncr_documents", verbose_name="Document")
    timestamp = models.DateTimeField(auto_now_add=True)

    site = models.CharField(max_length=200, verbose_name="site / location")
    customer = models.CharField(max_length=200, verbose_name="Customer")
    product_description = models.TextField(verbose_name="Product Description")
    product_part_number = models.CharField(max_length=200, verbose_name="Product Part No")
    issue_reported_stage = models.CharField(max_length=200, verbose_name="Issue Reported Stage")
    po_details = models.TextField(verbose_name="PO Details")
    product_rev = models.CharField(max_length=200, verbose_name="Product Rev")
    cyient_fg_number =  models.CharField(max_length=200, verbose_name="Cyient FG No")
    issued_by = models.CharField(max_length=200, verbose_name="Issued by")
    issued_to = models.CharField(max_length=200, verbose_name="Issued to")
    lot = models.CharField(max_length=200, verbose_name="LOT")
    lot_and_defect_status = models.CharField(max_length=200, verbose_name="LOT and Defect Status")

    # problem description

    image1 = models.ImageField(upload_to="ncr_images", default="ncr_images/no-image.jpeg", verbose_name="Image 01")
    image2 = models.ImageField(upload_to="ncr_images", default="ncr_images/no-image.jpeg", verbose_name="Image 02")
    circuit_reference_or_ref_designator = models.CharField(max_length=200, verbose_name="Circute Reference or REF Designator")
    number_of_defects = models.CharField(max_length=200, verbose_name="Number of Defects")

    # containment action

    containment_action = models.CharField(max_length=200, verbose_name="Containment Action")
    containment_resp = models.CharField(max_length=200, verbose_name="Resp")
    containment_date = models.DateField(verbose_name="Containment Date")

    # root cause analysis

    root_cause_analysis = models.CharField(max_length=200, verbose_name="Root Cause Analysis")

    why1 =  models.CharField(max_length=200, null=True, blank=True, verbose_name="Why")
    why1_man = models.CharField(max_length=200, null=True, blank=True, verbose_name="MAN")
    why1_method = models.CharField(max_length=200, null=True, blank=True, verbose_name="METHOD")
    why1_material = models.CharField(max_length=200, null=True, blank=True, verbose_name="MATERIAL")
    why1_machine = models.CharField(max_length=200, null=True, blank=True, verbose_name="MACHINE")

    why2 =  models.CharField(max_length=200, null=True, blank=True, verbose_name="Why")
    why2_man = models.CharField(max_length=200, null=True, blank=True, verbose_name="MAN")
    why2_method = models.CharField(max_length=200, null=True, blank=True, verbose_name="METHOD")
    why2_material = models.CharField(max_length=200, null=True, blank=True, verbose_name="MATERIAL")
    why2_machine = models.CharField(max_length=200, null=True, blank=True, verbose_name="MACHINE")

    why3 =  models.CharField(max_length=200, null=True, blank=True, verbose_name="Why")
    why3_man = models.CharField(max_length=200, null=True, blank=True, verbose_name="MAN")
    why3_method = models.CharField(max_length=200, null=True, blank=True, verbose_name="METHOD")
    why3_material = models.CharField(max_length=200, null=True, blank=True, verbose_name="MATERIAL")
    why3_machine = models.CharField(max_length=200, null=True, blank=True, verbose_name="MACHINE")

    why4 =  models.CharField(max_length=200, null=True, blank=True, verbose_name="Why")
    why4_man = models.CharField(max_length=200, null=True, blank=True, verbose_name="MAN")
    why4_method = models.CharField(max_length=200, null=True, blank=True, verbose_name="METHOD")
    why4_material = models.CharField(max_length=200, null=True, blank=True, verbose_name="MATERIAL")
    why4_machine = models.CharField(max_length=200, null=True, blank=True, verbose_name="MACHINE")

    why5 =  models.CharField(max_length=200, null=True, blank=True, verbose_name="Why")
    why5_man = models.CharField(max_length=200, null=True, blank=True, verbose_name="MAN")
    why5_method = models.CharField(max_length=200, null=True, blank=True, verbose_name="METHOD")
    why5_material = models.CharField(max_length=200, null=True, blank=True, verbose_name="MATERIAL")
    why5_machine = models.CharField(max_length=200, null=True, blank=True, verbose_name="MACHINE")

    how = models.CharField(max_length=200, verbose_name="How", null=True, blank=True)


    # corrective action

    corrective_action = models.CharField(max_length=200, verbose_name="Corrective Action")
    corrective_resp = models.CharField(max_length=200, verbose_name="Resp")
    corrective_date = models.DateField(verbose_name="Date")

    # preventive action

    preventive_action = models.CharField(max_length=200, verbose_name="Preventive Action")
    preventive_resp = models.CharField(max_length=200, verbose_name="Resp")
    preventive_date = models.DateField(verbose_name="Date")
   
   # verification for effectiveness

    wo_no = models.CharField(max_length=200, verbose_name="Wo No")
    batch_no = models.CharField(max_length=200, verbose_name="Batch No")
    verification_details = models.CharField(max_length=200, verbose_name="Verification Details")
    verification_status = models.CharField(max_length=200, verbose_name="Status")
    verification_resp = models.CharField(max_length=200, verbose_name="Resp")
    varifiction_date = models.DateField(verbose_name="Date")

    status = models.CharField(max_length=200, choices=status, default='Open')

    def __str__(self):
        return self.ncr_number



class POTracker(models.Model):
    project = models.CharField(max_length=200,null=True,blank=True)
    customer = models.CharField(max_length=200,null=True,blank=True)
    ship_to = models.CharField(max_length=200,null=True,blank=True)
    rafael_part_number = models.CharField(max_length=200,null=True,blank=True)
    cyient_part_number = models.CharField(max_length=200,null=True,blank=True)
    description = models.CharField(max_length=2000,null=True,blank=True)
    po_number = models.CharField(max_length=2000,null=True,blank=True)
    kras_po_number = models.CharField(max_length=2000,null=True,blank=True)
    poline = models.CharField(max_length=2000,null=True,blank=True, default='0')
    quantity = models.IntegerField(null=True,blank=True)
    unit_price = models.CharField(max_length=200,null=True,blank=True)
 
    consumed = models.IntegerField(default=0)
    remaining = models.IntegerField(default=0)
    add_quantity = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.po_number




class DlCustomer(models.Model):
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title


class DlProject(models.Model):
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title


class DlProductPartNumber(models.Model):
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title


class DlBriefDefectDescription(models.Model):
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title


class DlCustomerPartNumber(models.Model):
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title


class DlProductDescription(models.Model):
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title


class DlComplaintDescription(models.Model):
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title


class DlSourceofComplaint(models.Model):
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title


class DefectiveLibrary(models.Model):
    check1 = (
        ('YES', 'YES'),
        ('NO', 'NO')
    )
 
    customer = models.ForeignKey(DlCustomer, on_delete=models.PROTECT)
    project = models.ForeignKey(DlProject, on_delete=models.PROTECT)
    product_part_number = models.ForeignKey(DlProductPartNumber, on_delete=models.PROTECT)
    brief_defect_description = models.ForeignKey(DlBriefDefectDescription, on_delete=models.PROTECT)
    customer_part_number = models.ForeignKey(DlCustomerPartNumber, on_delete=models.PROTECT)
    product_rev = models.CharField(max_length=200, default='')
    product_description = models.ForeignKey(DlProductDescription, on_delete=models.PROTECT)
    complaint_description = models.CharField(max_length=2000, default='')
    source_of_complaint = models.ForeignKey(DlSourceofComplaint, on_delete=models.PROTECT)
    quantity_affected = models.IntegerField(default=0)
    original_date = models.DateField(verbose_name="Date Of Report", null=True, blank=True)
    reported_on = models.DateTimeField(auto_now_add=True)
    defect_image_available = models.CharField(max_length=200, choices=check1)
    defect_image = models.ImageField(upload_to='defects_images',blank=True,null=True)
    root_cause = models.CharField(max_length=2000)
    ca_pa = models.CharField( max_length=2000, verbose_name="CAPA")
    defect_cause = models.CharField(max_length=2000)

    class Meta:
        ordering = ['reported_on']


class SIShipped(models.Model):
    sl_no = models.IntegerField(null=True, blank=True)
    invoice_date = models.DateField(verbose_name="Invoice Date", null=True, blank=True)
    customer_part_number = models.CharField(max_length=200, verbose_name="Customer Part No", null=True, blank=True)
    cdlm_part_number = models.CharField(max_length=200, verbose_name="CDLM Part No", null=True, blank=True)
    invoice_no = models.CharField(max_length=200, verbose_name="Invoice No", null=True, blank=True)
    po_number = models.CharField(max_length=200, verbose_name="PO No", null=True, blank=True)
    customer = models.CharField(max_length=200, verbose_name="Customer", null=True, blank=True)
    serial_number = models.CharField(max_length=200, verbose_name="Serial Number", null=True, blank=True)
    quantity = models.IntegerField(verbose_name="Quantity", null=True, blank=True)
    remarks = models.CharField(max_length=200, verbose_name="Remarks", null=True, blank=True)
    



@receiver(pre_save, sender=SIShipped)
def set_sl_no(sender, instance, **kwargs):
    if not instance.sl_no:
        max_sl_no = SIShipped.objects.aggregate(models.Max('sl_no'))['sl_no__max']
        next_sl_no = max_sl_no + 1 if max_sl_no is not None else 1
        instance.sl_no = next_sl_no


@receiver(post_save, sender=SIShipped)
def add_all_si(sender, created, instance, **kwargs):
    if created:
        AllSIShipped.objects.create(
            sl_no = instance.sl_no,
            invoice_date = instance.invoice_date,
            customer_part_number = instance.customer_part_number,
            cdlm_part_number = instance.cdlm_part_number,
            invoice_no = instance.invoice_no,
            po_number = instance.po_number,
            customer = instance.customer,
            serial_number = instance.serial_number,
            quantity = instance.quantity,
            remarks = instance.remarks
        )


class AllSIShipped(models.Model):
    sl_no = models.IntegerField(null=True, blank=True)
    invoice_date = models.DateField(verbose_name="Invoice Date", null=True, blank=True)
    customer_part_number = models.CharField(max_length=200, verbose_name="Customer Part No", null=True, blank=True)
    cdlm_part_number = models.CharField(max_length=200, verbose_name="CDLM Part No", null=True, blank=True)
    invoice_no = models.CharField(max_length=200, verbose_name="Invoice No", null=True, blank=True)
    po_number = models.CharField(max_length=200, verbose_name="PO No", null=True, blank=True)
    customer = models.CharField(max_length=200, verbose_name="Customer", null=True, blank=True)
    serial_number = models.CharField(max_length=200, verbose_name="Serial Number", null=True, blank=True)
    quantity = models.IntegerField(verbose_name="Quantity", null=True, blank=True)
    remarks = models.CharField(max_length=200, verbose_name="Remarks", null=True, blank=True)


class Ncrdump(models.Model):
    project = models.CharField(max_length=200,verbose_name="Project",null=True, blank=True)
    date = models.CharField(max_length=200,verbose_name=" Date", null=True, blank=True)
    ncrno = models.CharField(max_length=200, verbose_name="NCR No", null=True, blank=True)
    ccaapp = models.CharField(max_length=200, verbose_name="CCA Applicable", null=True, blank=True)
    infgpn = models.CharField(max_length=200, verbose_name="Internal FG PN", null=True, blank=True)
    ponum = models.TextField( verbose_name="PO #", null=True, blank=True)
    ncrdetails = models.TextField( verbose_name="NCR Details", null=True, blank=True)
    proslno = models.CharField(max_length=200, verbose_name="Product Serial Number", null=True, blank=True)
    qa = models.CharField(max_length=200,verbose_name="Q&A", null=True, blank=True)
    ncrqty = models.IntegerField(verbose_name="NCR QTY", null=True, blank=True)
    poqty = models.IntegerField(verbose_name="PO QTY", null=True, blank=True)
    shipqty = models.IntegerField(verbose_name="SHIPPED QTY", null=True, blank=True)
    openqty = models.IntegerField(verbose_name="OPEN QTY", null=True, blank=True)
    add_qty = models.IntegerField(verbose_name="Add QTY", null=True, blank=True)
    ncrstatus = models.CharField(max_length=200,verbose_name="NCR status", null=True, blank=True)
    approvalstatus = models.CharField(max_length=200,verbose_name="Approval Status", null=True, blank=True)
    remarks = models.TextField(verbose_name="Remarks", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True,null=True,blank=True)








#class NCRTracker(models.Model):
#
#    ncr_status_choice = (
#        ('<-select->','<-select->'),
#        ('In_Progress', 'In_progress'),
#
#        ('Closed', 'Closed')
#
#    )
#
#    ncr_approval_status = (
#        ('<-select->','<-select->'),
#        ('Approved', 'Approved'),
#        ('Pending', 'Pending')
#
#    )
#
#    project = models.CharField(max_length=200)
#    serial_number = models.CharField(max_length=200)
#    date = models.DateField()
#    ncr_number = models.CharField(max_length=200)
#    customer_part_number = models.CharField(max_length=200)
#    internal_fg_partnumber = models.CharField(max_length=200)
#    po_number = models.CharField(max_length=200)
#    details = models.TextField()
#    quantity = models.IntegerField(default=0)
#    remaining = models.IntegerField(default=0)
#    consumed = models.IntegerField(default=0)
#    add_quantity = models.IntegerField(default=0)
#    ncr_status = models.CharField(max_length=200,  choices=ncr_status_choice)
#    approval_status = models.CharField(max_length=200, choices=ncr_approval_status)
#    approval_Date = models.DateField()
#    document = models.FileField(blank=True,null=True,upload_to="ncr_documents")
#    timestamp = models.DateTimeField(auto_now=True)
#
#    def __str__(self):
#        return self.ncr_number



#######################################  AC


