#import datetime
from haystack import indexes
from .models import Entry, Comment


class EntryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    description = indexes.CharField(model_attr='description')
    #content_auto = indexes.EdgeNgramField(model_attr='body')

    def get_model(self):
        return Entry

    def index_queryset(self, using=None):
        return self.get_model().load_all()
        # return self.get_model().objects.all()
        # return
        # self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())


class CommentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    description = indexes.CharField(model_attr='description')
    #content_auto = indexes.EdgeNgramField(model_attr='body')

    def get_model(self):
        return Comment

    def index_queryset(self, using=None):
        return self.get_model().load_all()
