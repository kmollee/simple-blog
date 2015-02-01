from django.apps import AppConfig
import watson

 
class BlogAppConfig(AppConfig):

    name = 'apps.blog'
    verbose_name = 'BLOG'

    def ready(self):
        Entry = self.get_model("Entry")
        watson.register(Entry, fields=("title", "description"))
        Comment = self.get_model("Comment")
        watson.register(Comment, fields=("title", "description",))
