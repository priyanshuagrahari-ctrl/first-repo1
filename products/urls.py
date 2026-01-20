from django.urls import path
from .views import product_list,product_by_id,product_list_cursor

urlpatterns = [

    path('list/', product_list, name='product-list'),
    path('byid/',product_by_id,name='product-list-byid'),
    path('list_cursor/',product_list_cursor,name='product_list_cursor')
]
