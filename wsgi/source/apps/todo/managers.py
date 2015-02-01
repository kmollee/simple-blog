from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet, EmptyQuerySet


class ListQuerySet(QuerySet):
    def specificUser(self, user):
        q = self.filter(author=user)
        return q
    
    def get_user_completed_items(self, user):
        q = self.filter(Q(list__completed=True) & Q(author=user))
        return q
    
    def get_user_uncompleted_items(self, user):
        q = self.filter(Q(list__completed=False) & Q(author=user))
        return q
class ListFkManager(models.Manager):
    
    def get_empty_query_set(self):
        return self.get_query_set().none()
    
    def get_queryset(self):
        return ListQuerySet(self.model, using=self._db)
    
    def aviable(self, user):
        return self.get_queryset().specificUser(user)
    
    def get_user_completed_items(self, user):
        return self.get_queryset().get_user_completed_items(user)

    def get_user_umcompleted_items(self, user):
        return self.get_queryset().get_user_umcompleted_items(user)
