from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registeration', views.registeration, name='registeration'),
    
    path('c_show_services', views.c_show_services, name='c_show_services'),
    path('c_add_service', views.c_add_service, name='c_add_service'),
    path('c_update_service/<int:pk>', views.c_update_service, name='c_update_service'),
    
    path('c_show_products', views.c_show_products, name='c_show_products'),
    path('c_add_product', views.c_add_product, name='c_add_product'),
    path('c_update_product/<int:pk>', views.c_update_product, name='c_update_product'),
    
    path('c_show_persons', views.c_show_persons, name='c_show_persons'),
    path('c_add_person', views.c_add_person, name='c_add_person'),
    path('c_update_person/<int:pk>', views.c_update_person, name='c_update_person'),
    
    path('c_show_purchases', views.c_show_purchases, name='c_show_purchases'),
    path('c_add_purchase', views.c_add_purchase, name='c_add_purchase'),
    path('load_product_by_id', views.load_product_by_id, name='load_product_by_id'),
    
    path('c_show_sales', views.c_show_sales, name='c_show_sales'),
    path('c_add_sale', views.c_add_sale, name='c_add_sale'),
    path('load_products_price', views.load_products_price, name='load_products_price'),
    path('load_products_quantity', views.load_products_quantity, name='load_products_quantity'),
    path('load_service_price', views.load_service_price, name='load_service_price'),
    
    path('invoice/<sale_id>', views.invoice, name='invoice'),
]