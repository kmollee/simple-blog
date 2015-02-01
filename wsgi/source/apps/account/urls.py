from __future__ import absolute_import
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from .views import IndexView, LoginView, LogoutView, CreateUser, ChangePassWordView, PasswordResetConfirmView, ResetPasswordRequestView
from django.conf import settings


urlpatterns = patterns(
    '',
    url(r'^index/$', IndexView.as_view(), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^changepassword/$', ChangePassWordView.as_view(),
        name='changepassword'),
)
if settings.OPEN_REGISTER:
    urlpatterns += patterns(
        '',
        url(r'^register/$', CreateUser.as_view(), name='register'),
    )
if settings.OPEN_FORGET_PASSWORD:
    urlpatterns += patterns(
        '',
        url(r'^reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
            PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
        url(r'^reset_password/$', ResetPasswordRequestView.as_view(),
            name="reset_password"),
    )
