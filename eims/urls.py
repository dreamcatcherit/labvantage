from django.conf.urls import url
from eims import views

urlpatterns = [
    url(r'^add_new_instrument/$', views.add_new_instrument, name="add_instrument"),
    url(r'^add_calibration_info/$', views.add_calibration_info, name="add_calibration_info"),
    url(r'^view_instrument/id/(?P<id>[^\.]+)/$', views.view_instrument, name="view_instrument"),
    url(r'^view_instruments/', views.view_instruments, name="view_instruments"),
    url(r'^view_internal_reports/', views.view_internal_reports, name="view_internal_reports"),
    url(r'^view_internal_report/id/(?P<id>[^\.]+)/$', views.view_internal_report, name="view_internal_report"),

    url(r'^schedule_calibration_tests/', views.schedule_calibration_tests, name="schedule_calibration_tests"),
    url(r'^view_calibration_tests/', views.view_calibration_tests, name="view_calibration_tests"),
    url(r'^view_calibration_test/id/(?P<id>[^\.]+)/$', views.view_calibration_test, name="view_calibration_test"),
    url(r'^view_calibration_info/id/(?P<id>[^\.]+)/$', views.view_calibration_info, name="view_calibration_info"),

]