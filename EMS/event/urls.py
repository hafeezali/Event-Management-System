from django.conf.urls import url
from . import views

app_name = 'event'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^add_event/$', views.add_event, name='add_event'),
    url(r'^(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'update/(?P<pk>[0-9]+)/$', views.UpdateEvent.as_view(), name='update_event'),
    url(r'profile/(?P<pk>[0-9]+)/$', views.get_user_profile, name='user_profile'),
    url(r'past_events/$', views.get_past_events, name='past_events'),
    url(r'add_money/(?P<pk>[0-9]+)/$', views.add_money, name='add_money'),
    url(r'withdraw_money/(?P<pk>[0-9]+)/$', views.withdraw_money, name='withdraw_money'),
    url(r'buy_ticket/(?P<pk>[0-9]+)/$', views.buy_ticket, name='buy_ticket'),
    url(r'invite_users/(?P<pk>[0-9]+)/$', views.invite_users, name='invite_users')
]