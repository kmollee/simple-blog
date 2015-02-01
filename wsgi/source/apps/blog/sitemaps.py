from django.contrib.sitemaps import Sitemap
from .models import Entry

class EntrySiteMap(Sitemap):
    changefreq = 'daily'
    priority = 0.4
    
    def items(self):
        return Entry.objects.all()
    def lastmod(self, obj):
        return obj.submitted_on
    def location(self, obj):
        return obj.get_absolute_url()
