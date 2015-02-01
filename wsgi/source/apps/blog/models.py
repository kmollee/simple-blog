from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Count


class AbstractTagManager(models.Manager):

    def by_entrys(self):
        qs = super().get_queryset()
        return qs.annotate(entry_count=Count('entry')).order_by('-entry_count')


class Tag(models.Model):
    title = models.CharField("Title", max_length=50, unique=True)
    objects = AbstractTagManager()

    def __str__(self):
        return self.title

    def getTitle(self):
        return self.title

    def getRelateEntry(self):
        return self.entry_set.all()

    def getModelName(self):
        """
        get instance's model name
        """
        return self.__class__.__name__

    def get_absolute_url(self):
        return reverse('blog:tag:tagToEntry', kwargs={'pk': self.id})

    def get_update_url(self):
        return reverse('blog:tag:update', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('blog:tag:delete', kwargs={'pk': self.id})

    @classmethod
    def getTop(cls):
        return cls.objects.all().annotate(
            entry_count=Count('entry'))[:5]

    @classmethod
    def getAnnotate(cls):
        return cls.objects.all().annotate(entry_count=Count('entry'))


class Entry(models.Model):
    title = models.CharField("Headline", max_length=100)
    submitter = models.ForeignKey(User)
    submitted_on = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    tag = models.ManyToManyField(Tag, blank=True)

    class Meta:
        ordering = ('-id', '-submitted_on')

    def __str__(self):
        return self.title

    def getTitle(self):
        return self.title

    def getSubmitter(self):
        return self.submitter

    def getSubmittedOn(self):
        return self.submitted_on

    def getDescription(self):
        return self.description

    def getRelateTags(self):
        """
        get all relate tag
        """
        return self.tag.all()

    def getRelateComments(self):
        return self.comment_set.all()

    def get_absolute_url(self):
        return reverse('blog:entry:detail', kwargs={'pk': self.id})

    def get_update_url(self):
        return reverse('blog:entry:update', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('blog:entry:delete', kwargs={'pk': self.id})

    def getModelName(self):
        """
        get instance's model name
        """
        return self.__class__.__name__

    def is_owner(self, user):
        return self.submitter == user

    @classmethod
    def getAnnotate(cls):
        return cls.objects.all().annotate(comment_count=Count('comment'))


class Comment(models.Model):
    title = models.CharField("Headline", max_length=100)
    submitter = models.ForeignKey(User, blank=True)
    submitted_on = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    entry = models.ForeignKey(Entry, blank=True, default=None)

    class Meta:
        ordering = ('-submitted_on',)

    def __str__(self):
        return self.title

    def getTitle(self):
        return self.title

    def getSubmitter(self):
        return self.submitter

    def getSubmittedOn(self):
        return self.submitted_on

    def getDescription(self):
        return self.description

    def getRelateEntry(self):
        return self.entry

    def getModelName(self):
        """
        get instance's model name
        """
        return self.__class__.__name__

    def get_absolute_url(self):
        return reverse('blog:comment:detail', kwargs={'pk': self.id})

    def get_relate_entry_url(self):
        return self.entry.get_absolute_url()

    def get_update_url(self):
        return reverse('blog:comment:update', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('blog:comment:delete', kwargs={'pk': self.id})

    def is_owner(self, user):
        return self.submitter == user
