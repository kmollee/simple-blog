from django.db import models
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
import datetime
from django.contrib.auth.models import User
from . import managers
from utils import uniqueSlugify


class List(models.Model):
    objects = managers.ListFkManager()
    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=60, editable=False)
    author = models.ForeignKey(
        User,
        related_name='todo_list',
    )

    def save(self, *args, **kwargs):
        if not self.id:
            slug_str = "%s %s" % (self.author.username, self.name)
            #print(slug_str) 
            uniqueSlugify.unique_slugify(self, slug_str)
            #print(self.slug)
        super().save(*args, **kwargs)
    
    @classmethod
    def serialize_field(cls):
        return("name",)
        
    def __str__(self):
        return self.name


    def getTitle(self):
        return self.name

    def is_owner(self, user):
        return self.author == user
    
    def get_relate_items(self):
        return self.item_set.all()

    def incomplete_tasks(self):
        # Count all incomplete tasks on the current list instance
        return Item.objects.filter(list=self, completed=False)
        
    def incomplete_tasks_count(self):
        # Count all incomplete tasks on the current list instance
        return self.incomplete_tasks().count()
    
    def complete_tasks(self):
        return Item.objects.filter(list=self, completed=True)

    def complete_tasks_count(self):
        return self.complete_tasks().count()
        
    def get_absolute_url(self):
        return reverse('todo:list:detail', kwargs={'slug':self.slug})
    
    def get_update_url(self):
        return reverse('todo:list:update', kwargs={'slug':self.slug})

    def get_delete_url(self):
        return reverse('todo:list:delete', kwargs={'slug':self.slug})
    
    def getModelName(self):
        return self.__class__.__name__
        
    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Lists"

        # Prevents (at the database level) creation of two lists with the same name in the same group
        unique_together = ("slug",)
class Item(models.Model):
    LOW = 0
    MIDDLE = 1
    HIGH = 2
    Priority_CHOICES = (
        (LOW, 'LOW'),
        (MIDDLE, 'MIDDLE'),
        (HIGH, 'HIGH'),
    )
    title = models.CharField(max_length=140)
    list = models.ForeignKey(List)
    created_date = models.DateField(auto_now_add=True)
    #due_date = models.DateField(blank=True, null=True, )
    completed = models.BooleanField(default=False)
    #completed_date = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='todo_created_by')
    note = models.TextField(blank=True, null=True)
    priority = models.PositiveIntegerField(
        max_length=2, choices=Priority_CHOICES, default=MIDDLE)

    # Model method: Has due date for an instance of this object passed?
    # def overdue_status(self):
    #     "Returns whether the item's due date has passed or not."
    #     if self.due_date and datetime.date.today() > self.due_date:
    #         return 1
    @classmethod
    def serialize_field(cls):
        return("title", "note", "priority")
    def getTitle(self):
        return self.title

    def get_relate_list_url(self):
        return self.list.get_absolute_url()

    # def get_relate_comments(self):
    #     return self.comment_set.all()

    def get_absolute_url(self):
        return reverse('todo:item:detail', kwargs={'pk': self.id})

    def get_update_url(self):
        return reverse('todo:item:update', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('todo:item:delete', kwargs={'pk': self.id})

    def get_toggle_url(self):
        return reverse('todo:item:toggle', kwargs={'pk': self.id})

    def get_ajax_update_url(self):
        return reverse('todo:item:ajaxUpdate', kwargs={'pk':self.id})
    
    def __str__(self):
        return self.title

    def getModelName(self):
        return self._meta.verbose_name

    # Auto-set the item creation / completed date
    # def save(self):
    # If Item is being marked complete, set the completed_date
    #     if self.completed:
    #         self.completed_date = datetime.datetime.now()
    #     super().save()

    def is_owner(self, user):
        return self.created_by == user

    class Meta:
        ordering = ["completed", "-priority"]
# class Comment(models.Model):
#     """
#     Not using Django's built-in comments because we want to be able to save
#     a comment and change task details at the same time. Rolling our own since it's easy.
#     """
#     author = models.ForeignKey(User, related_name='todo_comment')
#     task = models.ForeignKey(Item)
#     date = models.DateTimeField(default=datetime.datetime.now)
#     body = models.TextField(blank=True)

#     def is_owner(self, user):
#         return self.author == user

#     def get_relate_task_url(self):
#         return self.task.get_absolute_url()

#     def get_update_url(self):
#         return reverse('todo:comment:update', kwargs={'pk': self.id})

#     def get_delete_url(self):
#         return reverse('todo:comment:delete', kwargs={'pk': self.id})

#     def getModelName(self):
#         return self.__class__.__name__

#     def getTitle(self):
#         return 'Comment to ' + self.task.getTitle() + ' on ' + str(self.date)

#     def snippet(self):
# Define here rather than in __str__ so we can use it in the admin list_display
# return "{author} - {snippet}...".format(author=self.author,
# snippet=self.body[:35])

#     def __str__(self):
#         return self.snippet()
