from django.urls import path
from . import  views


app_name='venapp'
urlpatterns = [
    path('',views.index1,name='index1'),
    path('list/',views.list,name='list'),
    path('det/<int:v_id>/',views.details,name='details'),
     path('delete/<int:id>/',views.delete,name='delete'),
    path('edit/<int:id>/',views.edit,name='edit'),
     path('porder/',views.po,name='po'),
     path('list_orders/',views.list_orders,name='list_orders'),
      path('od/<int:od_id>/',views.orderdetail,name='orderdetail'),
    path('update/<int:id>/',views.updateorder,name='updateorder'),
    path('deleteorder/<int:id>/',views.delete_order,name='delete_order'),
   path('index/',views.index,name='index'),
     path('vendor/<int:vendor_id>/on_time_delivery_rate/', views.on_time_delivery_rate_view, name='on_time_delivery_rate_view'),


]
