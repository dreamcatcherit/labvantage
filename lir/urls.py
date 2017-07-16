from django.conf.urls import url
from lir import views

urlpatterns = [
    url(r'^$', views.create_new_lrf, name='create_new_lrf'),
    url(r'^sampler/$', views.sampler),
    url(r'^lab_manager/(?P<slug>[^\.]+)/$', views.lab_manager),
    url(r'^verifier/(?P<slug>[^\.]+)/$', views.verifier),
    url(r'^sampler_approved_list/$', views.sampler_approved_list),
    url(r'^verifier_list/$', views.verifier_list),
    url(r'^lab_manager_list/$', views.lab_manager_list),
    url(r'^sampler_pending_list/$', views.sampler_pending_list),
    url(r'^sampler_pending_list/(?P<slug>[^\.]+)/$', views.sampler_pending_list),
    url(r'^report/$', views.select_report),
    url(r'^report/(?P<slug>[^\.]+)/$', views.report),
    url(r'^report_save/$', views.report_save),
    url(r'^report_verify/$', views.report_verify),
    url(r'^report_verify_save/$', views.report_verify_save),
    url(r'^view_lrf/$', views.view_lrf, name="view_lrf"),
    url(r'^pending/$', views.pending, name="view_pending"),
    url(r'^verified/$', views.verified, name="view_verified"),
    url(r'^approved/$', views.approved, name="view_approved"),
    url(r'^rejected/$', views.rejected, name="view_rejected"),
    url(r'^reference_number/(?P<slug>[^\.]+)/$', views.reference_number, name='view_reference'),
    url(r'^view_lir/$', views.view_lir, name="view lir"),
    url(r'^view_lir/id/(?P<pk>[^\.]+)/$', views.view_lir_by_id, name="view_lir_by_id"),
    url(r'^view_released/$', views.view_released, name="view_released"),
    url(r'^released/id/(?P<id>[^\.]+)/$', views.view_release_certificate, name='view_released'),
    url(r'^report_approved_save/$', views.report_approved_save, name="approved_save"),
    url(r'^release/$', views.release, name="release"),

]
