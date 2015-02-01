from __future__ import absolute_import
from django.contrib import admin
from .models import Entry, Tag, Comment
from pagedown.widgets import AdminPagedownWidget
from django.db import models




@admin.register(Entry)
class EntryListAdmin(admin.ModelAdmin):
    list_display = ('title', 'submitter', 'submitted_on')
    list_filter = ('submitter',)
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }



admin.site.register(Tag)
admin.site.register(Comment)
