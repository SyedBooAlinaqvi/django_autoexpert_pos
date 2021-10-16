from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='index'),
    path('master', views.master, name='master'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('show_services', views.show_services, name='show_services'),
    path('add_service', views.add_service, name='add_service'),
    path('update_service/<int:pk>', views.update_service, name='update_service'),
    path('del_service/<int:pk>', views.del_service, name='del_service'),
    path('show_products', views.show_products, name='show_products'),
    path('add_product', views.add_product, name='add_product'),
    path('update_product/<int:pk>', views.update_product, name='update_product'),
    path('del_product/<int:pk>', views.del_product, name='del_product'),
    path('show_persons', views.show_persons, name='show_persons'),
    path('add_person', views.add_person, name='add_person'),
    path('update_person/<int:pk>', views.update_person, name='update_person'),
    path('show_purchases', views.show_purchases, name='show_purchases'),
    path('add_purchase', views.add_purchase, name='add_purchase'),
    path('load_product_by_id', views.load_product_by_id, name='load_product_by_id'),
    path('show_sales', views.show_sales, name='show_sales'),
    path('add_sale', views.add_sale, name='add_sale'),
    path('load_products_price', views.load_products_price, name='load_products_price'),
    path('load_products_quantity', views.load_products_quantity, name='load_products_quantity'),
    path('load_service_price', views.load_service_price, name='load_service_price'),
    path('show_ledger', views.show_ledger, name='show_ledger'),
    path('invoice/<sale_id>', views.invoice, name='invoice'),
]