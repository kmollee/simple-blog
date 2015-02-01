from django.shortcuts import render, HttpResponse, redirect
from django.http import Http404
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from . import forms
from . import models
from django.core.urlresolvers import reverse_lazy
import json
from django.db.models import Count
from django.contrib import messages
from django.views.generic.detail import SingleObjectMixin
from utils.decorators import my_login_required
from utils import mixins
import watson
from django.conf import settings
"""
class LoggedInMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            raise Http404
        return super(LoggedInMixin, self).dispatch(request, *args, **kwargs)
"""


class CommonMixin(object):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagside'] = models.Tag.objects.by_entrys()[:5]
        # context['tagform'] = forms.TagForm(
        #    action=reverse_lazy('blog:tag:ajaxUpdate'))
        return context

"""
def user_permitted(function):
    def decorator(function):
        def _wrapped_view(request, *args, **kwargs):
            # get obj from request
            if obj.user != request.user or (not request.user.is_superuser):
                return HttpResponseRedirect(reverse('forbidden'))
            return function(request, *args, **kwargs)
        return _wrapped_view
    return decorator(function)
"""


class EntryMixin(CommonMixin):

    """
    Entry Mixin
    model : Entry
    queryset: add annotate, count relate comment ammounts
    """
    queryset = models.Entry.objects.all()


class EntryListView(EntryMixin, mixins.PaginatorMixin, ListView):

    """
    List all Entry
    """
    #model = models.Entry
    queryset = models.Entry.getAnnotate()
    template_name = "blog/index.html"
    context_object_name = "entrys"


class EntryDetailView(EntryMixin, SingleObjectMixin, ListView):

    """
    Entry Detail
    accept comment post
    comment Form init the title to relate Entry title

    if comment post is ok, redirect to relate Entry
    """
    form_class = forms.CommentForm
    template_name = "blog/entryDetail.html"
    paginate_by = 5
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        # here set we want to query(Tag model), overridden get_object's
        # queryset
        self.object = self.get_object(queryset=models.Entry.getAnnotate())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entry'] = self.object
        context['form'] = self.form_class(
            title=('RE:' + self.object.getTitle()))
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            messages.add_message(
                self.request, messages.SUCCESS, 'comment create success')
            #obj = self.get_object()
            obj = self.get_object(queryset=models.Entry.objects.all())
            form.save(submitter=request.user, entry=obj)
            return redirect(obj)
        else:
            return self.get(request, *args, **kwargs)

    def get_queryset(self):
        # get the entry relate comments
        # print('call')
        return self.object.comment_set.all()


class EntryCreateView(mixins.LoginRequiredMixin, EntryMixin, CreateView):

    """
    Entry Create
    """
    model = models.Entry
    form_class = forms.EntryForm
    template_name = "blog/form.html"

    def form_valid(self, form):
        self.object = form.save(submitter=self.request.user)
        return redirect(self.object)


class EntryUpdateView(mixins.OwnerOrSuperuserMixin, EntryMixin, UpdateView):

    """
    Entry Create
    """
    form_class = forms.EntryForm
    model = models.Entry
    template_name = "blog/form.html"


class EntryDeleteView(mixins.OwnerOrSuperuserMixin, EntryMixin, DeleteView):
    model = models.Entry
    success_url = reverse_lazy('blog:entry:list')
    form_class = forms.EntryForm
    template_name = "blog/comfirm_delete.html"


class TagMixin(CommonMixin):
    form_class = forms.TagForm
    queryset = models.Tag.objects.all()


class TagListView(TagMixin, ListView):
    template_name = "blog/tagList.html"
    context_object_name = "tags"
    queryset = models.Tag.getAnnotate()


class TagEntryListView(TagMixin, SingleObjectMixin, mixins.PaginatorMixin, ListView):

    """
    Entry queryset for use by ListView
    Tag queryset for use in get_object() will call get
    get_object() default will call get_queryset(), but it is not I want
    overridden return Entry instead of Tag
    """
    paginate_by = 10
    template_name = "blog/tagEntryList.html"

    def get(self, request, *args, **kwargs):
        # here set we want to query(Tag model)
        self.object = self.get_object(queryset=models.Tag.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.object
        return context

    def get_queryset(self):
        # get the tag relate entrys
        return self.object.entry_set.all().annotate(comment_count=Count('comment'))


class TagCreateView(mixins.SuperUserCheckMixin, TagMixin, CreateView):

    template_name = "blog/form.html"


class TagUpdateView(mixins.SuperUserCheckMixin, TagMixin, UpdateView):
    # success_url = reverse_lazy('blog:entry:list')
    template_name = "blog/form.html"


class TagDeleteView(mixins.SuperUserCheckMixin, TagMixin, DeleteView):
    success_url = reverse_lazy('blog:tag:list')
    template_name = "blog/comfirm_delete.html"


class NoTagEntryListView(EntryMixin, mixins.PaginatorMixin, ListView):
    template_name = "blog/tagEntryList.html"
    context_object_name = "entrys"
    queryset = models.Entry.objects.filter(tag=None).annotate(
        comment_count=Count('comment'))
    paginate_by = '10'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = 'NO SELECT TAG'
        return context
"""
@login_required
def ajaxUpdateTag(request):
    if request.method == 'POST' and request.is_ajax():
        tagname = request.POST['title']
        tag, status = models.Tag.objects.get(title=tagname)
        if status:
            tag.title = tagname
            tag.save()
            return HttpResponse(json.dumps({'error': 'false', 'message': 'update success', 'tagname': tag.title}))
        else:
            return HttpResponse(json.dumps({'error': 'true', 'message': 'tag exist, try another.'}))
    else:
        raise Http404
"""


class CommentMixin(CommonMixin):
    model = models.Comment
    form_class = forms.CommentForm


class CommentDetailView(CommentMixin, DeleteView):
    template_name = "blog/commentDetail.html"
    context_object_name = "comment"


class CommentUpdateView(mixins.OwnerOrSuperuserMixin, CommentMixin, UpdateView):
    template_name = "blog/form.html"

    def get_success_url(self):
        return self.object.get_relate_entry_url()


class CommentDeleteView(mixins.OwnerOrSuperuserMixin, CommentMixin, DeleteView):
    template_name = 'blog/comfirm_delete.html'

    def get_success_url(self):
        return self.object.get_relate_entry_url()


if settings.SEARCH_ENGINE == 'HAYSTACK':
    #from haystack.forms import HighlightedSearchForm, ModelSearchForm
    from haystack.views import SearchView, search_view_factory
    from haystack.query import SearchQuerySet

    sqs = SearchQuerySet().models(models.Entry)

    class MySearch(CommonMixin, SearchView):

        def extra_context(self):
            context = {}
            context['tagside'] = models.Tag.objects.by_entrys()[:5]
            return context

    def search(request):
        sqs = SearchQuerySet().models(models.Entry, models.Comment)
        view = search_view_factory(
            view_class=MySearch,
            template='blog/search.html',
            searchqueryset=sqs,
            form_class=HighlightedSearchForm
        )
        return view(request)
else:
    class WatsonSearchListView(CommonMixin, mixins.PaginatorMixin, ListView):

        """
        search comment and entry
        """
        template_name = "blog/watson_search.html"
        #context_object_name = "entrys"
        models = (models.Entry, models.Comment)

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            print(self.request.GET.get('q', None))
            context['form'] = forms.SearchForm(q=self.request.GET.get('q'))
            return context

        def get_models(self):
            return self.models

        def get_queryset(self):
            """
            Return the list of items for this view.
            The return value must be an iterable and may be an instance of
            `QuerySet` in which case `QuerySet` specific behavior will be enabled.
            """
            query_string = self.request.GET.get('q')
            if query_string:
                result = watson.search(query_string, models=self.get_models())
                return result
            # return empty query set
            return models.Entry.objects.none()
