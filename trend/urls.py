from django.conf.urls import url
from trend import views
urlpatterns = [
    url(r'^$', views.trend, name="trend"),
]