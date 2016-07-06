from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^qa_form/', views.audit, name='qa_form'),
    url(r'^machine_list/', views.machine_list, name='machine_list'),
    url(r'^search/', views.search, name='search'),
    url(r'^machine_detail_search/', views.machine_detail, name='machine_detail_search'),
    url(r'^new_machine_form/', views.new_machine, name='new_machine'),
    url(r'^report_issued/', views.report_issued, name='report_issued'),
    ]