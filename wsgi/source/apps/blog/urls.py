from __future__ import absolute_import
from django.conf.urls import patterns, url, include
from . import views
from django.conf import settings

entry_patterns = patterns(
    '',
    url(r'^$', views.EntryListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', views.EntryDetailView.as_view(), name='detail'),
    url(r'^create/$', views.EntryCreateView.as_view(), name='create'),
    url(r'^update/(?P<pk>\d+)/$',
        views.EntryUpdateView.as_view(), name='update'),
    url(r'^delete/(?P<pk>\d+)/$',
        views.EntryDeleteView.as_view(), name='delete'),
)
tag_patterns = patterns(
    '',
    url(r'^$', views.TagListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', views.TagEntryListView.as_view(),
        name='tagToEntry'),
    url(r'^create/$', views.TagCreateView.as_view(), name='create'),
    url(r'^update/(?P<pk>\d+)/$',
        views.TagUpdateView.as_view(), name='update'),
    url(r'^delete/(?P<pk>\d+)/$',
        views.TagDeleteView.as_view(), name='delete'),
    url(r'^notag/$', views.NoTagEntryListView.as_view(), name='noTagList'),
)
comment_patterns = patterns(
    '',
    url(r'^(?P<pk>\d+)/$', views.CommentDetailView.as_view(),
        name='detail'),
    url(r'^update/(?P<pk>\d+)/$', views.CommentUpdateView.as_view(),
        name='update'),
    url(r'^delete/(?P<pk>\d+)/$', views.CommentDeleteView.as_view(),
        name='delete'),
)


urlpatterns = patterns(
    '',
    url(r'^entry/', include(entry_patterns, namespace='entry')),
    url(r'^tag/', include(tag_patterns, namespace='tag')),
    url(r'^comment/', include(comment_patterns, namespace='comment')),

    #url(r'^search/$', views.MySearch, name='search')
)
if settings.SEARCH_ENGINE == 'HAYSTACK':
    urlpatterns += patterns(
        '',
        url(r'^search/$', views.search, name='search'),
    )
else:
    urlpatterns += patterns(
        '',
        url(r'^search/$', views.WatsonSearchListView.as_view(), name='search'),
    )
