from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import RedirectView
from apps.blog.sitemaps import EntrySiteMap

urlpatterns = patterns(
    '',
    url(r'^blog/', include('apps.blog.urls', namespace='blog')),
    url(r'^account/', include('apps.account.urls', namespace='account')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', RedirectView.as_view(pattern_name = 'blog:entry:list'), name="index"),
    url(r'^todo/', include('apps.todo.urls', namespace='todo')),
)

if settings.SEARCH_ENGINE == 'HAYSTACK':
    urlpatterns += patterns(
        '',
        url(r'^search/', include('haystack.urls')),
    )

# debug toolbar
# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += patterns(
#         '',
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     )

sitemaps = {
    'blog': EntrySiteMap,
}
urlpatterns += (
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)
