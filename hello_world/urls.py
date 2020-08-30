from django.urls import path
from hello_world import views
from django.conf.urls import url


urlpatterns = [
    path('', views.hello_world, name='hello_world'),
    url(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),
    url(r'^ajax/validate_registration/$', views.validate_registration, name='validate_registration'),
    url(r'^ajax/mail_receive/$', views.mail_receive, name='mail_receive'),
    url(r'^ajax/add_offender/$', views.add_offender, name='add_offender'),
    url(r'^ajax/add_trusted_contact/$', views.add_trusted_contact, name='add_trusted_contact'),
    url(r'^ajax/change_email/$', views.change_email, name='change_email'),
    url(r'^ajax/change_number/$', views.change_number, name='change_number'),
    url(r'^ajax/change_password/$', views.change_password, name='change_password'),
    url(r'^ajax/change_username/$', views.change_username, name='change_username'),
    url(r'^ajax/get_contacts/$', views.get_contacts, name='get_contacts'),
    url(r'^ajax/discarding/$', views.discarding, name='discarding'),
    url(r'^signup/$', views.SignUpView.as_view(), name='signup'),


]