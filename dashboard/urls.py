from django.urls import path
from dashboard import views 



urlpatterns = [
    path('si-plan', views.si_plan_view, name="si-plan"),
    path('update-siplan/<int:pk>', views.update_si_plan_view, name="update-siplan"),
    path('serial-number', views.serial_number_view, name="serial-number"),
    path('get-serial-numbers', views.get_serial_numbers, name='get-serial-numbers'),
    path('si_plan_export/', views.si_plan_export, name='si_plan_export'),
    path('serial_number_export/', views.serial_number_export, name="serial_number_export"),
    path('serial-mapping', views.serial_mapping_view, name="serial-mapping"),
    path('ncr-tracking', views.ncr_tracking_view, name="ncr-tracking"),
    path('add-ncr-tracking', views.add_ncr_tracking_view, name="add-ncr-tracking"),
    path('ncr_dump', views.ncr_dump_view, name="ncr_dump"),
    path('update_ncrdump_view/<int:pk>', views.update_ncrdump_view, name="update_ncrdump_view"),
    path('update-ncr-tracking/<int:pk>', views.update_ncr_tracking_view, name="update-ncr-tracking"),
    path('po-tracking', views.po_tracking_view, name="po-tracking"),
    path('export-po-tracker', views.po_tracker_export, name="export_po_tracker"),
    path('add-po-tracking', views.add_po_tracking_view, name="add-po-tracking"),
    path('update-po-tracking/<int:pk>', views.update_po_tracking_view, name="update-po-tracking"),
    path('defect-library', views.defect_library_view, name="defect-library"),
    path('add-defect-library', views.add_defect_library_view, name="add_defect_library"),
    path('defect-library-details/<int:pk>', views.defect_library_details_view, name="defect_library_details"),
    path('update-defect-library/<int:pk>', views.update_defect_library_view, name="update_defect_library"),
    #path('si-shipped', views.si_shipped_view, name="si-shipped"),
    path('si-shipped', views.search_sishipped, name="si-shipped"),
    path('add-si-shipped', views.add_si_shipped, name="add-si-shipped"),
    path('delete-shipped', views.delete_shipped_excel_view, name="delete-shipped"),
    path('export-ncr-data-to-excel/', views.ExportNCRDataToExcel.as_view(), name='export_ncr_data_to_excel'),
    path('export-ncr-data/', views.ExportNCRData.as_view(), name='export_ncr_data'),
    path('demo-excel/<int:pk>', views.demo_excel, name="demo_excel"),
    path('upload/', views.upload_excel, name='upload_excel'),
    path('upload_excel/', views.upload_excel_view, name='upload_excel_view'),
    path('upload_excelpo/', views.upload_excel_po, name='upload_excel_po'),
    


    path('csv', views.import_data_from_csv, name='csv'),

]