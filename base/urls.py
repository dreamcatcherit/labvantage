from django.conf.urls import url
from django.contrib.auth import views
from base.views import home, create_user, view_users

urlpatterns = [
    url(r'^login$', views.login, {'template_name': 'base/login.html'}, name="login"),
    url(r'^logout/$', views.logout, {'next_page': '/login'}, name="logout"),
    url(r'^home/$', home, name="home"),
    url(r'^$', home),
    url(r'^create_user/$', create_user, name="create_user"),
    url(r'^view_users/$', view_users, name="view_users"),
]