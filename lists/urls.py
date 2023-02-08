from django.urls import path, re_path
from lists import views

urlpatterns = [
    re_path(r'^$', views.home_page, name='home'),
    re_path(r'^new$', views.new_list2, name='new_list'),
    re_path(r'^(\d+)/$', views.view_list, name='view_list'),
    re_path(r'user/(.+)/$', views.user_lists, name='user_lists'),
]
