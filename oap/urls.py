from django.conf.urls import url
from oap import views

urlpatterns = [
    url(r'^create_new_oap/$', views.create_new_oap, name="create_new_oap"),
    url(r'^view_oap_reports/$', views.view_oap_reports, name="view_oap_reports"),
    url(r'^view_oap_report/id/(?P<id>[^\.]+)/$', views.view_oap_report, name="view_oap_report"),

]