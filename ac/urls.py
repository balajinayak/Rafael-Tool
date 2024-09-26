from django.urls import path
from ac import views


urlpatterns = [
    #path('home', views.index_view, name="home"),
    path('master-data/', views.master_data, name='master_data'),
    path('add-dummy/', views.add_dummy, name='add_dummy'),
    path('work-order', views.work_order, name='work_order'),
    path('ac/', views.ac_view, name='ac'),
    path('get-fg-data/', views.get_fg_data, name='get_fg_data'),
    path('front-paage/<int:pk>', views.front_page, name='front_page'),
    path('export/', views.export_view, name='export'),
    path('serial-export/', views.serial_export, name='serial_export'),
    path('wip', views.wip_report_view, name='wip'),
    path('export/excel/', views.export_to_excel, name='export_to_excel'),
    path('update-master/', views.update_master_view, name='update_master'),
    path('get-serials/<str:fg>/<str:wo>/<int:ord>/<int:qty>', views.get_serials, name="get_serials"),
]