from django.conf.urls import url
from inventory import views

urlpatterns = [
    url(r'^add_new_product$', views.add_new_product, name='add_new_product'),
    url(r'^add_new_customer$', views.add_new_customer, name='add_new_customer'),
    url(r'^add_new_equipment$', views.add_new_equipment, name='add_new_equipment'),
    url(r'^add_new_oap_test$', views.add_new_oap_test, name='add_new_oap_test'),
    url(r'^add_new_test$', views.add_new_test, name='add_new_test'),
    url(r'^add_test_info', views.add_test_info, name='add_test_info'),
    url(r'^view_products_test_list', views.view_products_test_list, name='view_products_test_list'),
    url(r'^view_products', views.view_products, name='view_products'),
    url(r'^view_tests', views.view_tests, name='view_tests'),
    url(r'^view_customers', views.view_customers, name='view_customers'),
    url(r'^view_customer/id/(?P<id>[^\.]+)/$', views.view_customer, name='view_customer'),
    url(r'^view_equipments', views.view_equipments, name='view_equipments'),
    url(r'^view_oap_tests', views.view_oap_tests, name='view_oap_tests'),
    url(r'^view_equipment/id/(?P<id>[^\.]+)/$', views.view_equipment, name='view_equipment'),

]
