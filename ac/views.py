from django.shortcuts import render, redirect, get_object_or_404
from django.http import QueryDict
from django.http import JsonResponse, HttpResponse
from .models import FG, Dummy, TestingModel, Stage
from accounts.models import CustomUser
from datetime import datetime, timedelta
from django.utils import timezone
from .forms import DummyForm, FGForm
import re
from django.contrib import messages
from .decorators import superuser_required, supervisor_required, no_supervisor_required
from django.contrib.auth.decorators import login_required
from django.db.models import Q


#@login_required
#def index_view(request):
#    context = {
#        }
#    return render(request, 'index.html', context)


@login_required
def master_data(request):
    form = DummyForm()
    stages = Stage.objects.all().order_by('id')
    context = {
        'form': form,
        'stages': stages,
        }
    return render(request, 'ac/master_data.html', context)



def add_dummy(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = DummyForm(request.POST)
            if form.is_valid():
                user = request.user
                fg_number = form.cleaned_data.get('fg_number')
                doc_ref_no = form.cleaned_data.get('doc_ref_no')
                checklist_rev_no = form.cleaned_data.get('checklist_rev_no')
                customer = form.cleaned_data.get('customer')
                product_desc = form.cleaned_data.get('product_desc')
                product = form.cleaned_data.get('product')
                pro_rev = form.cleaned_data.get('pro_rev')
                project_name = form.cleaned_data.get('project_name')
                security = form.cleaned_data.get('security')
                marking = request.POST.get('marking')
                common_remarks = request.POST.get('common_remarks')
                aps = request.POST.getlist('aps')
                in_pdf = request.POST.getlist('in_pdf')
                order = request.POST.getlist('order')
                pdf_order = request.POST.getlist('pdf_order')
                para = request.POST.getlist('para')
                description = request.POST.getlist('description')
                remarks = request.POST.getlist('remarks')
                position = request.POST.getlist('position')
                process = request.POST.getlist('process')

                for o, po, d, r, p, pro, pa, ap , ip in zip(order, pdf_order, description, remarks, position, process, para, aps, in_pdf):
                    Dummy.objects.create(
                        user=user,
                        fg_number=fg_number,
                        doc_ref_no=doc_ref_no,
                        checklist_rev_no=checklist_rev_no,
                        customer=customer,
                        product_desc=product_desc,
                        product=product,
                        pro_rev=pro_rev,
                        project_name=project_name,
                        security=security,
                        marking=marking,
                        common_remarks=common_remarks,
                        aps=ap,
                        in_pdf=ip,
                        order=o,
                        pdf_order=po,
                        para=pa,
                        description=d,
                        remarks=r,
                        position=p,
                        process=pro
                    )

                messages.success(request, 'Data added successfully')
                return JsonResponse({'success': True})

            else:
                errors = {field: form[field].errors for field in form.fields}
                return JsonResponse({'success': False, 'errors': errors})
    else:
        messages.error(request, 'Admin only can submit')
    return render(request, 'ac/master_data.html', {'fg_err' : fg_err})


@login_required
def work_order(request):
    get_fg_number = request.GET.get('get_fg_number')
    get_work_order = request.GET.get('get_work_order')
    fg_number = request.POST.get('fg_number')
    fg_list = Dummy.objects.values_list('fg_number', flat=True).order_by('-fg_number').distinct('fg_number')
    work_list = FG.objects.values_list('work_order', flat=True).order_by('-work_order').distinct('work_order')
    serial_list = FG.objects.values_list('serial', flat=True).order_by('-serial').distinct('serial')
    dummy = Dummy.objects.filter(fg_number=fg_number).first()
    fg_model = FG.objects.filter(fg_number=get_fg_number).first()
    all_dummy = Dummy.objects.filter(fg_number=fg_number)
    common = FG.objects.filter(fg_number=get_fg_number, work_order=get_work_order, process="common_process", submited=False).order_by('para').first()
    non_submit_common = FG.objects.filter(fg_number=get_fg_number, work_order=get_work_order, process="common_process", submited=False).order_by(
        'para').distinct('para')[1:]
    submit_common = FG.objects.filter(fg_number=get_fg_number, work_order=get_work_order, process="common_process", submited=True).order_by(
        'para').distinct('para')
    test_data = TestingModel.objects.all().first()
    serial_error = False

    form = FGForm(request.POST)

    if 'add_work_order' in request.POST and 'work_order_submit' in request.POST.get('add_work_order'):
        if request.user.is_superuser or request.user.is_supervisor:
            if form.is_valid():
                user = request.user
                fg_number = dummy.fg_number
                doc_ref_no = dummy.doc_ref_no
                checklist_rev_no = dummy.checklist_rev_no
                customer = dummy.customer
                product_desc = dummy.product_desc
                product = dummy.product
                pro_rev = dummy.pro_rev
                project_name = dummy.project_name
                security = dummy.security
                common_remarks = dummy.common_remarks
                aps = [items.aps for items in all_dummy]
                in_pdf = [items.in_pdf for items in all_dummy]
                order = [items.order for items in all_dummy]
                pdf_order = [items.pdf_order for items in all_dummy]
                para = [items.para for items in all_dummy]
                description = [items.description for items in all_dummy]
                remarks = [items.remarks for items in all_dummy]
                position = [items.position for items in all_dummy]
                process = [items.process for items in all_dummy]
                work_order = form.cleaned_data.get('work_order')
                start = form.cleaned_data.get('starting')
                wo_quantity = form.cleaned_data.get('wo_quantity')
                end = form.cleaned_data.get('ending')
                s = int(re.sub(r'\D', '', start))
                e = int(re.sub(r'\D', '', end))
                t = re.sub(r'\d', '', end)

                ser_list = []

                for num in range(s, e + 1):
                    if num < 10:
                        serial = "CDL" + str(num)
                        ser_list.append(serial[:-4] + "-" + serial[-4:])
                    else:
                        serial = "CDL" + str(num)
                        ser_list.append(serial[:-4] + "-" + serial[-4:])
                print(ser_list)
                set1 = set(ser_list)

                set2 = set(FG.objects.values_list('serial', flat=True))

                duplicate_numbers = set1.intersection(set2)
                print(duplicate_numbers)

                if duplicate_numbers:
                    serial_error = True
                else:
                    serial_error = False

                if not serial_error:
                    for num in range(s, e + 1):
                        if num < 10:
                            serial = "CDL" + str(num)
                            serial = serial[:-4] + "-" + serial[-4:]
                        else:
                            serial = "CDL" + str(num)
                            serial = serial[:-4] + "-" + serial[-4:]
                        for o, po, pa, d, r, p, pro, ap, ip in zip(order, pdf_order, para, description, remarks, position, process, aps, in_pdf):

                            FG.objects.create(
                                user=user,
                                fg_number=fg_number,
                                doc_ref_no=doc_ref_no,
                                checklist_rev_no=checklist_rev_no,
                                customer=customer,
                                product_desc=product_desc,
                                product=product,
                                pro_rev=pro_rev,
                                project_name=project_name,
                                security=security,                                          
                                work_order=work_order,
                                starting=start,
                                wo_quantity=wo_quantity,
                                ending=end,
                                serial=serial,
                                common_remarks=common_remarks,
                                aps=ap,
                                in_pdf=ip,
                                order=o,
                                pdf_order=po,
                                para=pa,
                                description=d,
                                remarks=r,
                                position=p,
                                process=pro,
                            )


                    messages.success(request, 'Work Order added successfully')
                    return redirect('work_order')
                else:
                    messages.success(request, 'something wrong')
    else:
        form = FGForm()



    if request.method == 'POST':
        if 'common_submit' in request.POST and 'commonSubmit' in request.POST.get('common_submit'):
            id = request.POST.get('id')
            common_note = request.POST.get('common_note')
            data = FG.objects.get(id=id)
            all_common = FG.objects.filter(fg_number=data.fg_number, process="common_process", order=data.order)
            user_instance = CustomUser.objects.get(username=request.user)

            update_next_fg(request, data)

            try:
                for ac in all_common:
                    if ac.position == 'both':
                        if request.user.position == 'operator':
                            ac.operator_submit_user = request.user
                            ac.operator_timestamp = timezone.now()
                        else:
                            ac.submited = True
                            ac.inspector_submit_user = request.user
                            ac.inspector_timestamp = timezone.now()
                    else:
                        ac.submited = True
                        if ac.position == 'operator':
                            ac.operator_submit_user = request.user
                            ac.operator_timestamp = timezone.now()
                        else:
                            ac.inspector_submit_user = request.user
                            ac.inspector_timestamp = timezone.now()
                    ac.save()
                
                if data.order == 1:
                    ind_fg = FG.objects.filter(fg_number=data.fg_number, work_order=data.work_order, process="individual_process").order_by('order').first()
                    all_ind_fg = FG.objects.filter(fg_number=data.fg_number, work_order=data.work_order, process="individual_process", order=ind_fg.order).order_by('order')
                    for ai in all_ind_fg:
                        if ai.quantity == 0:
                            ai.quantity = data.wo_quantity
                            ai.save()
                else:
                    pass

                user_instance.is_submit = True
                current_time = timezone.now()
                user_instance.is_submit_time = current_time + timedelta(seconds=5)
                user_instance.save()
                test_model = TestingModel.objects.all().first()
                test_model.test = True
                test_model.test_time = current_time + timedelta(seconds=5)
                test_model.save()

                try:
                    if common_note:
                        work_orders = FG.objects.filter(work_order=data.work_order, para=data.para)
                        for w in work_orders:
                            if w.serial >= data.serial:
                                q = FG.objects.get(id=w.id)
                                q.common_note = common_note
                                q.save()
                except:
                    print('common note not submitted')
            except:
                print('something wrong')
            query_params = request.GET.urlencode()
            messages.success(request, 'Data submitted successfully')
            return redirect(f"{request.path}?{query_params}")


        if request.method == 'POST':
            if 'customer_submit' in request.POST and 'customerSubmit' in request.POST.get('customer_submit'):
                if request.user.is_superuser or request.user.is_supervisor:
                    cus_serial = request.POST.get('customer_serial')
                    cus_part_number = request.POST.get('customer_part_number')
                    cus_serials = FG.objects.filter(serial=cus_serial)
                    cus_serials_exists = FG.objects.filter(serial=cus_serial).first()
                    if cus_serials:
                        if cus_serials_exists.customer_part_number:
                            messages.error(request, 'Customer PartNo already exists')
                        else:
                            for cus in cus_serials:
                                cus.customer_part_number = cus_part_number
                                cus.save()
                            messages.success(request, 'Customer PartNo added successfully')
                
    context = {
        'form': form,
        'dummy': dummy,
        'fg_model': fg_model,
        'common': common,
        'fg_list': fg_list,
        'work_list': work_list,
        'non_submit_common': non_submit_common,
        'submit_common': submit_common,
        'serial_error': serial_error,
        'get_fg_number': get_fg_number,
        'get_work_order': get_work_order,
        'test_data': test_data,
        'serial_list': serial_list,
    }
    return render(request, 'ac/work_order.html', context)



@login_required
def ac_view(request):
    serial = request.GET.get('serial')
    ser = FG.objects.filter(serial=serial).first()
    work_order = ser.work_order if ser else ""
    fg_number = ser.fg_number if ser else ""
    common_note = request.POST.get('common_note')
    work_list =  FG.objects.values_list('work_order', flat=True).order_by('-work_order').distinct('work_order')
    fg_list = Dummy.objects.values_list('fg_number', flat=True).order_by('-fg_number').distinct('fg_number')
    ser_list = FG.objects.values_list('serial', flat=True).order_by('-serial').distinct('serial')
    individual = FG.objects.filter(fg_number=fg_number,work_order=work_order,serial=serial,process="individual_process",submited=False).order_by('para').first()
    non_submit_individual = FG.objects.filter(work_order=work_order,fg_number=fg_number,serial=serial,process="individual_process",submited=False).order_by('para').distinct('para')[1:]
    submit_individual = FG.objects.filter(work_order=work_order,fg_number=fg_number,serial=serial,process="individual_process",submited=True).order_by('para').distinct('para')
    common_data_submited = FG.objects.filter(work_order=work_order,fg_number=fg_number,serial=serial,process='common_process', submited=True).order_by('para').distinct('para')
    test_data = TestingModel.objects.all().first()

    is_common = False
    common_list = []
    common_data = FG.objects.filter(fg_number=fg_number,serial=serial,process='common_process')
    for com in common_data:
        if com.submited:
            common_list.append(True)
    
    if len(common_data) == len(common_list):
        is_common = True

    if request.method == 'POST':
        if 'individual_submit' in request.POST and 'individualSubmit' in request.POST.get('individual_submit'):
            id = request.POST.get('id')
            data = FG.objects.get(id=id)
            user_instance = CustomUser.objects.get(username=request.user)

            update_next_fg(request, data)

            try:
                if data.position == 'both':
                    if request.user.position == 'operator':
                        data.operator_submit_user = request.user
                        data.operator_timestamp = timezone.now()
                    else:
                        data.submited = True
                        data.inspector_submit_user = request.user
                        data.inspector_timestamp = timezone.now()
                else:
                    data.submited = True
                    if request.user.position == "operator":
                        data.operator_submit_user = request.user
                        data.operator_timestamp = timezone.now()
                    elif request.user.position == "inspector":
                        data.inspector_submit_user = request.user
                        data.inspector_timestamp = timezone.now()
                    else:
                        print('wrong user')

                data.save()
                #user_instance.is_submit = True
                current_time = timezone.now()
                #user_instance.is_submit_time = current_time + timedelta(seconds=5)
                #user_instance.save()
                test_model = TestingModel.objects.all().first()
                test_model.test = True
                test_model.test_time = current_time + timedelta(seconds=5)
                test_model.save()
                data_querysets = FG.objects.filter(serial=data.serial)
                for dq in data_querysets:
                    dq.today_submit_user.add(request.user)
                    dq.today_submit_timestamp = current_time
                    dq.save()

                messages.success(request, 'Data submitted successfully')
                
                try:
                    if common_note:
                        work_orders = FG.objects.filter(work_order=data.work_order, para=data.para)
                        for w in work_orders:
                            if w.serial >= data.serial:
                                q = FG.objects.get(id=w.id)
                                q.common_note = common_note
                                q.save()
                        messages.success(request, 'Successfully submitted with Component Consumption ')
                except:
                    print('common note not submitted')
            except:
                print('something wrong')

            update_first_order(data)

            query_params = request.GET.urlencode()
            #return redirect(f"{request.path}?{query_params}")
            return redirect('ac')
    
    context = {
        'individual': individual,
        'work_list': work_list,
        'fg_list': fg_list,
        'ser_list': ser_list,
        'work_order': work_order,
        'fg_number': fg_number,
        'serial': serial,
        'non_submit_individual': non_submit_individual,
        'submit_individual': submit_individual,
        'is_common': is_common,
        'common_data_submited': common_data_submited,
        'test_data': test_data,
    }
    return render(request, 'ac/ac.html', context)


def update_first_order(data):
    if data.submited:
        first_order = FG.objects.filter(fg_number=data.fg_number, work_order=data.work_order, process="individual_process").order_by('order').first()
        if first_order.order == data.order:
            submitted_order = FG.objects.filter(fg_number=data.fg_number, work_order=data.work_order, order=first_order.order, process="individual_process")
            next_fgs_sample = FG.objects.filter(fg_number=data.fg_number, work_order=data.work_order, order__gt=first_order.order, process="individual_process").first()
            next_fgs = ''
            if next_fgs_sample:
                next_fgs = FG.objects.filter(fg_number=next_fgs_sample.fg_number, work_order=next_fgs_sample.work_order, order=next_fgs_sample.order, process="individual_process")
            for sub in submitted_order:
                if sub.quantity < 0:
                    sub.quantity = 0
                    sub.save()
                else:
                    sub.quantity = int(sub.quantity) - 1
                    sub.save()
            if next_fgs:
                for nf in next_fgs:
                    nf.quantity = int(nf.quantity) + 1
                    nf.save()
        else:
            current_order = FG.objects.filter(fg_number=data.fg_number, work_order=data.work_order, order=data.order, process="individual_process")
            for co in current_order:
                if co.quantity < 0:
                    co.quantity = 0
                    co.save()
                else:
                    co.quantity = int(co.quantity) - 1
                    co.save()
            try:
                next_order_sample = FG.objects.filter(fg_number=data.fg_number, work_order=data.work_order, order__gt=data.order, process="individual_process").first()
                next_order = FG.objects.filter(fg_number=next_order_sample.fg_number, work_order=next_order_sample.work_order, order=next_order_sample.order, process="individual_process")
                if next_order:
                    for no in next_order:
                        no.prev_submit_serial = True
                        no.quantity = int(no.quantity) + 1
                        no.save()
            except:
                pass



def update_next_fg(request, data):
    try:
        next_data = FG.objects.filter(fg_number=data.fg_number,work_order=data.work_order,order=int(data.order)+1)
        if next_data:
            for nd in next_data:
                nd.prev_submit_serial = True
                nd.prev_submit = True
                nd.save()
    except:
        messages.error(request, "something went wrong in getting future submiting data")


from django.core.serializers import serialize
import json
def get_fg_data(request):
    wo_js_data = serialize('json', FG.objects.order_by('work_order').distinct('work_order'))
    return JsonResponse(wo_js_data, safe=False)

def front_page(request, pk):
    fg = FG.objects.get(id=pk)
    mark = Dummy.objects.filter(fg_number=fg.fg_number).first()
    context = {
        'fg': fg,
        'marking': mark,
    }
    return render(request, 'ac/first_page.html', context)


import re


def export_view(request):
    fg_number = request.GET.get('fg_number')
    work_order = request.GET.get('work_order')
    serial = request.GET.get('serial')

    serial_search = None

    submitted_serials = []

    if serial:
        all_serial = FG.objects.filter(submited=True, serial=serial).order_by('serial').distinct('serial')
        for als in all_serial:
            order_count = Dummy.objects.filter(fg_number=als.fg_number).count()
            serials_orders = FG.objects.filter(serial=als.serial, submited=True).count()
            if order_count == serials_orders:
                submitted_serials.append(als.serial)

        serials_set = set(submitted_serials)
        serial_nums = list(serials_set)
        serials = []

        fg_list = []
        work_order_list = []
        serial_list = []

        for serial in serial_nums:
            serials = []
            serials.append(FG.objects.filter(serial=serial).first())

        for s in serials:
            fg_list.append(s.fg_number)
            work_order_list.append(s.work_order)
            serial_list.append(s.serial)

    else:

        all_serial = FG.objects.filter(submited=True).order_by('serial').distinct('serial')
        for als in all_serial:
            order_count = Dummy.objects.filter(fg_number=als.fg_number).count()
            serials_orders = FG.objects.filter(serial=als.serial, submited=True).count()
            if order_count == serials_orders:
                if als.customer_part_number:
                    submitted_serials.append(als.serial)

        serials_set = set(submitted_serials)
        serial_nums = list(serials_set)
        serials = []

        fg_list = []
        work_order_list = []
        serial_list = []

        for serial in serial_nums:
            serials.append(FG.objects.filter(serial=serial).first())

        for s in serials:
            fg_list.append(s.fg_number)
            work_order_list.append(s.work_order)
            serial_list.append(s.serial)

        
    context = {
        'serials': serials,
        'serial': serial,
        'serial_search': serial_search,
        'fg_list': fg_list,
        'work_order_list': work_order_list,
        'serial_list': serial_list,
    }
    return render(request, 'ac/export.html', context)




import pdfkit
import barcode
from barcode import Code128
from django.http import HttpResponse
from django.shortcuts import render
import base64

#def generate_barcode_svg(barcode_value):
#    # Generate barcode SVG data
#    code128 = Code128(barcode_value, writer=barcode.writer.SVGWriter())
#    return code128.render().decode('utf-8')


@login_required
def serial_export(request):
    if request.method == 'POST':
        serial = request.POST.get('export_serial')
    if request.user.is_superuser or request.user.is_supervisor:
        serials = FG.objects.filter(serial=serial,in_pdf="in_pdf").order_by('pdf_order')
        fg = FG.objects.filter(serial=serial).first()
        common_note = FG.objects.filter(serial=serial).order_by('common_note').distinct('common_note')
        common_note_length = FG.objects.order_by('common_note').distinct('common_note').count()
        remarks = FG.objects.filter(serial=serial).order_by('remarks').distinct('remarks')
        dummy = Dummy.objects.filter(fg_number=fg.fg_number).first()

        #barcode_values = [fg.product, fg.pro_rev, fg.serial]
        #barcode_svgs = []

        #for barcode_value in barcode_values:
        #    barcode_svgs.append(generate_barcode_svg(barcode_value))

        unique_data = []
        seen = set()
        for item in serials:
            key = (item.get_remarks_number(), item.get_remarks_text())
            if key not in seen:
                unique_data.append(item)
                seen.add(key)

        context = {
            'fg': fg,
            'data': serials,
            'unique': unique_data,
            #'barcode_svgs': barcode_svgs,
            'common_note': common_note,
            'common_note_length': common_note_length,
            'remarks': remarks,
            'dummy': dummy,
        }

        # Render the HTML template
        html_template = 'ac/serial_export.html'
        rendered_html = render(request, html_template, context)

        # Convert bytes-like object to string
        html_content = rendered_html.content.decode('utf-8')

        # Convert HTML to PDF
        config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
        pdf = pdfkit.from_string(html_content, False, configuration=config)

        # Return PDF as a response
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{ serial }_{fg.timestamp}.pdf"'

        return response


@login_required
def wip_report_view(request):
    filters = Q(process="individual_process")

    work_order = request.GET.get('work_order')
    if work_order:
        filters &= Q(work_order=work_order)
    
    serial = request.GET.get('serial')
    if serial:
        filters &= Q(serial=serial)
    
    fg_number = request.GET.get('fg_number')
    if fg_number:
        filters &= Q(fg_number=fg_number)
    
    description = request.GET.get('description')
    if description:
        filters &= Q(description=description)
        

    date_filter = request.GET.get('date')
    if date_filter:
        try:
            date_filter = datetime.strptime(date_filter, "%Y-%m-%d").date()
            filters &= Q(update__date=date_filter)
        except ValueError:
            pass
        
    #all_data = FG.objects.filter(filters).values(
    #    'work_order', 'serial', 'fg_number', 'description', 'quantity'
    #).distinct('work_order', 'description').order_by('-work_order', 'description', '-update')[:1500]

    f = FG.objects.all().order_by('-update').first()

    if f is not None:
        all_data = FG.objects.filter(filters, fg_number=f.fg_number).values(
            'work_order', 'serial', 'fg_number', 'wo_quantity', 'description', 'quantity'
        ).distinct('work_order').order_by('-work_order', '-update')[:1500]
    else:
        all_data = []


    fg = FG.objects.all().distinct('fg_number')
    wo = FG.objects.all().distinct('work_order')
    des = FG.objects.all().distinct('description')

    all_stages = Stage.objects.all().order_by('id')

    fgs = FG.objects.filter(process="individual_process").order_by('work_order','description').distinct('work_order','description')

    data = FG.objects.filter(filters).values(
        'work_order', 'serial', 'fg_number', 'wo_quantity', 'description', 'quantity'
    ).distinct('work_order').order_by('-work_order', '-update')[:1500]


    data_list = []

    for ad in data:
        stages = Stage.objects.all().order_by('description')
        fg_stages = FG.objects.filter(fg_number=ad['fg_number'], work_order=ad['work_order'], process="individual_process").order_by('description').distinct('description')
        
        stage_list = []

        for s in stages:
            for fs in fg_stages:
                if s.description == fs.description:
                    stage_list.append(fs)



        data_list.append({
            'fg_number' : ad['fg_number'],
            'work_order' : ad['work_order'],
            'wo_quantity' : ad['wo_quantity'],
            'serial' : ad['serial'],
            'description' : ad['description'],
            'quantity' : ad['quantity'],
            'stages' : stage_list,
        })

    context = {
        'all_data': all_data,
        'fg': fg,
        'wo': wo,
        'des': des,
        'stages': all_stages,
        'fgs': fgs,
        'data_list': data_list,
    }

    return render(request, 'ac/wip_report.html', context)



from django.http import JsonResponse

def get_serials(request, fg, wo, ord, qty):
    serial_numbers = FG.objects.filter(fg_number=fg, work_order=wo, order=ord, submited=False).order_by('serial').values_list('serial', flat=True).distinct()[:qty]
    serials = list(serial_numbers)
    return JsonResponse(serials, safe=False)



@login_required
def export_to_excel(request):

    filters = Q(process="individual_process")

    start_date = request.GET.get('start_date')
    if start_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            filters &= Q(update__date__gte=start_date)
        except ValueError:
            pass

    end_date = request.GET.get('end_date')
    if end_date:
        try:
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            filters &= Q(update__date__lte=end_date)
        except ValueError:
            pass

    work_order = request.GET.get('work_order')
    if work_order:
        filters &= Q(work_order=work_order)
    
    serial = request.GET.get('serial')
    if serial:
        filters &= Q(serial=serial)
    
    fg_number = request.GET.get('fg_number')
    if fg_number:
        filters &= Q(fg_number=fg_number)
    
    description = request.GET.get('description')
    if description:
        filters &= Q(description=description)
        

    date_filter = request.GET.get('date')
    if date_filter:
        try:
            date_filter = datetime.strptime(date_filter, "%Y-%m-%d").date()
            filters &= Q(update__date=date_filter)
        except ValueError:
            pass
        
    #all_data = FG.objects.filter(filters).values(
    #    'work_order', 'serial', 'fg_number', 'description', 'quantity'
    #).distinct('work_order', 'description').order_by('-work_order', 'description', '-update')[:1500]

    f = FG.objects.all().order_by('-update').first()

    if f is not None:
        all_data = FG.objects.filter(filters, fg_number=f.fg_number).values(
            'work_order', 'serial', 'fg_number', 'wo_quantity', 'description', 'quantity'
        ).distinct('work_order').order_by('-work_order', '-update')[:1500]
    else:
        all_data = []


    fg = FG.objects.all().distinct('fg_number')
    wo = FG.objects.all().distinct('work_order')
    des = FG.objects.all().distinct('description')

    all_stages = Stage.objects.all().order_by('id')

    fgs = FG.objects.filter(process="individual_process").order_by('work_order','description').distinct('work_order','description')

    data = FG.objects.filter(filters).values(
        'work_order', 'serial', 'fg_number', 'wo_quantity', 'description', 'quantity'
    ).distinct('work_order').order_by('-work_order', '-update')[:1500]


    data_list = []

    for ad in data:
        stages = Stage.objects.all().order_by('description')
        fg_stages = FG.objects.filter(fg_number=ad['fg_number'], work_order=ad['work_order'], process="individual_process").order_by('description').distinct('description')
        
        stage_list = []

        for s in stages:
            for fs in fg_stages:
                if s.description == fs.description:
                    stage_list.append(fs)



        data_list.append({
            'fg_number' : ad['fg_number'],
            'work_order' : ad['work_order'],
            'wo_quantity' : ad['wo_quantity'],
            'serial' : ad['serial'],
            'description' : ad['description'],
            'quantity' : ad['quantity'],
            'stages' : stage_list,
        })

    queryset = FG.objects.filter(filters).values(
                    'fg_number', 'work_order', 'description', 'quantity'
                ).distinct('work_order', 'description').order_by('work_order', 'description', '-update')

    context = {
        'all_data': all_data,
        'fg': fg,
        'wo': wo,
        'des': des,
        'stages': all_stages,
        'fgs': fgs,
        'data_list': data_list,
        'queryset': queryset,
    }

    return render(request, 'ac/wip_export.html', context)



@superuser_required
def update_master_view(request):
    get_serial = request.GET.get('serial')
    fg = FG.objects.filter(serial=get_serial).first()

    if fg:
        mark_fg = Dummy.objects.filter(fg_number=fg).first()
        form = DummyForm(instance=mark_fg)
    else:
        form = DummyForm()


    rows = FG.objects.filter(fg_number=fg, serial=get_serial).order_by('order').distinct('order')

    if request.method == 'POST':
        if get_serial:
            marking = request.POST.get('marking')
            marks = Dummy.objects.filter(fg_number=fg)
            if marks:
                for m in marks:
                    m.marking = marking
                    m.save()
            fg_number = request.POST.get('fg_number')
            doc_ref_no = request.POST.get('doc_ref_no')
            serial = request.POST.get('serial')
            chk_rev = request.POST.get('checklist_rev_no')
            pro_rev = request.POST.get('pro_rev')
            customer = request.POST.get('customer')
            product_desc = request.POST.get('product_desc')
            product = request.POST.get('product')
            project_name = request.POST.get('project_name')
            security = request.POST.get('security')

            common_remarks = request.POST.get('common_remarks')
            order = request.POST.getlist('order')
            description = request.POST.getlist('description')
            remarks = request.POST.getlist('remarks')
            aps = request.POST.getlist('aps')
            pdf_check = request.POST.getlist('in_pdf')
            position= request.POST.getlist('position')
            process = request.POST.getlist('process')

            serials = FG.objects.filter(fg_number=fg_number, serial__gte=fg.serial).order_by('serial')

            if any(param in [fg_number, doc_ref_no, chk_rev, pro_rev, customer, product_desc, product, project_name, security] for param in [None, '']):
                messages.error(request, 'Please fill in all required fields.')
                return render(request, 'ac/update_master.html')

            if serials:
                for s in serials:
                    s.fg_number = fg_number
                    s.doc_ref_no = doc_ref_no
                    s.checklist_rev_no = chk_rev
                    s.pro_rev = pro_rev
                    s.customer = customer
                    s.product_desc = product_desc
                    s.product = product
                    s.project_name = project_name
                    s.security = security
                    s.common_remarks = common_remarks

                    for o, d, r, a, ip, po, pr in zip(order, description, remarks, aps, pdf_check, position, process):
                        ord = FG.objects.filter(order=o, fg_number=s.fg_number, serial__gte=fg.serial)
                        for orr in ord:
                            orr.description = d
                            orr.remarks = r
                            orr.aps = a
                            orr.in_pdf = ip
                            orr.position = po
                            orr.process = pr
                            orr.save()

                    s.save()
                messages.success(request, 'Data updated successfully...')
                return redirect('update_master')
            else:
                messages.error(request, 'Please check all fields...')
        else:
            messages.error(request, 'Invalid serial Number...')

    context={
        'field' : fg,
        'form' : form,
        'rows' : rows,
    }

    return render(request, 'ac/update_master.html', context)