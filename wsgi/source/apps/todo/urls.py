from __future__ import absolute_import
from django.conf.urls import patterns, include, url
from . import views


List_patterns = patterns(
    '',
    # list all List
    url(r'^list/$', views.ListListView.as_view(), name='list'),
    # show the List contain Item
    url(r'^detail/(?P<slug>[-\w]+)/$', views.ListDetailView.as_view(), name='detail'),
    # url(r'^create/$', views.ListCreateView.as_view(), name='create'),
    url(r'^update/(?P<slug>[-\w]+)/$', views.ListUpdateView.as_view(), name='update'),
    url(r'^delete/(?P<slug>[-\w]+)/$', views.ListDeleteView.as_view(), name='delete'),
)
Item_patterns = patterns(
    '',
    url(r'^detail/(?P<pk>\d+)/$',
        views.ItemDetailView.as_view(), name='detail'),
    url(r'^update/(?P<pk>\d+)/$',
        views.ItemUpdateView.as_view(), name='update'),
    url(r'^delete/(?P<pk>\d+)/$',
        views.ItemDeleteView.as_view(), name='delete'),
    url(r'^ajax/toggle/(?P<pk>\d+)/$', views.itemToggle, name='toggle'),
    url(r'^ajax/update/(?P<pk>\d+)/$', views.AjaxUpdateView.as_view(), name='ajaxUpdate'),
)
#Comment_patterns = patterns(
#    '',
#    url(r'^update/(?P<pk>\d+)/$',
#        views.CommentUpdateView.as_view(), name='update'),
#    url(r'^delete/(?P<pk>\d+)/$',
#        views.CommentDeleteView.as_view(), name='delete'),
#)


urlpatterns = patterns(
    '',
    url(r'^list/', include(List_patterns, namespace='list')),
    url(r'^item/', include(Item_patterns, namespace='item')),
)
