from django.shortcuts import render, redirect, HttpResponse
from django.views.generic.base import TemplateView, View, RedirectView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from . import models
from . import forms
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from utils import mixins
from django.db.models import Count
import json
from django.core import serializers
from django.views.generic import View
from utils.mixins import RequireSignInAjax
from utils.mixins import JSONResponseMixin
from utils.mixins import HybridFormResponseMixin, HybridResponseMixin
from crispy_forms.utils import render_crispy_form
from django.views.generic.edit import FormMixin

class ListListView(mixins.LoginRequiredMixin, FormMixin, ListView):
    model = models.List
    template_name = "todo/List_list.html"
    context_object_name = "lists"
    form_class = forms.ListForm
    success_url = 'todo:list:list'
    
    def get_queryset(self):
        return models.List.objects.aviable(self.request.user)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            messages.add_message(
                self.request, messages.SUCCESS, 'List create success')
            obj = form.save(submitter=request.user)
            return redirect(reverse(self.success_url))
        else:
            return self.get(request, *args, **kwargs)

class ListDetailView(mixins.OwnerOrSuperuserMixin, HybridFormResponseMixin, HybridResponseMixin, FormMixin, DetailView):
    model = models.List
    template_name = "todo/List_detail.html"
    context_object_name = "list"
    form_class = forms.ItemForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context['form'] = form
        return context
    
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            messages.add_message(
                self.request, messages.SUCCESS, 'Item create success')
            obj = form.save(list_obj=self.get_object(), submitter=request.user)
            self.success_url = obj.list.get_absolute_url()
            return super().form_valid(form)
        else:
            #return self.get(request, *args, **kwargs)
            return super().form_is_invalid(form)
class ListCreateView(mixins.LoginRequiredMixin, CreateView):
    model = models.List
    template_name = 'todo/form.html'
    form = forms.ListForm
class ListUpdateView(mixins.OwnerOrSuperuserMixin, UpdateView):
    model = models.List
    form_class = forms.ListForm
    template_name = 'todo/form.html'
class ListDeleteView(mixins.OwnerOrSuperuserMixin, DeleteView):
    model = models.List
    success_url = reverse_lazy('todo:list:list')
    form_class = forms.ListForm
    template_name = 'todo/delete_form.html'
from django.http import JsonResponse
class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response
class ItemDetailView(mixins.OwnerOrSuperuserMixin, HybridResponseMixin, DetailView, FormView):
    model = models.Item
    template_name = "todo/Item_detail.html"
    context_object_name = "item"
    # form_class = forms.CommentForm

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['commentform'] = self.form_class
    #     return context

    # def post(self, request, *args, **kwargs):
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     if form.is_valid():
    #         messages.add_message(
    #             self.request, messages.SUCCESS, 'comment create success')
    #         obj = form.save(task=self.get_object(), submitter=request.user)
    #         return redirect(obj.list)
    #     else:
    #         return self.get(request, *args, **kwargs)
class ItemUpdateView(mixins.OwnerOrSuperuserMixin, HybridResponseMixin, HybridFormResponseMixin, UpdateView):
    model = models.Item
    form_class = forms.ItemForm
    template_name = 'todo/form.html'

    def get_success_url(self):
        return self.get_object().get_relate_list_url()
        
    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        kwargs.update({'action':self.object.get_update_url()})
        return kwargs
class ItemDeleteView(mixins.OwnerOrSuperuserMixin, HybridResponseMixin,HybridFormResponseMixin, DeleteView):
    model = models.Item
    form_class = forms.ItemForm
    template_name = 'todo/delete_form.html'
    
    def get_success_url(self):
        return self.get_object().get_relate_list_url()
from django.core.serializers.json import DjangoJSONEncoder


def itemToggle(request, pk):
    if request.method == 'POST':
        item = models.Item.objects.get(pk=pk)
        if item:
            item.completed = not item.completed
            item.save()
            if request.is_ajax():
                response_data = {}
                response_data['result'] = 'edit item successful!'
                # tasks = models.Item.objects.filter(created_by=request.user)
                # task_list = [{"pk": task.id, "title": task.title, "note":
                #               task.note, "completed": task.completed} for task in tasks]
                # response_data['task_list'] = task_list
                status = 200
            else:
                return redirect(item.get_relate_list_url())
        else:
            if request.is_ajax():
                response_data['result'] = 'edit item fail!'
                status = 404
            else:
                messages.add_message(
                    self.request, messages.ERROR, 'The Item is not exist')
                return redirect(request.META.get('HTTP_REFERER'))
        return HttpResponse(json.dumps(response_data, cls=DjangoJSONEncoder), content_type="application/json", status=status)
class AjaxUpdateView(RequireSignInAjax, JSONResponseMixin, UpdateView):
    model = models.Item
    form_class = forms.ItemForm

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = render_crispy_form(self.form_class)
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
# update and delete view

#class CommentUpdateView(mixins.OwnerOrSuperuserMixin, UpdateView):
#    model = models.Comment
#    form_class = forms.CommentForm
#    template_name = 'todo/form.html'
#
#    def get_success_url(self):
#        return self.get_object().get_relate_task_url()
#class CommentDeleteView(mixins.OwnerOrSuperuserMixin, DeleteView):
#    model = models.Comment
#    form_class = forms.CommentForm
#    template_name = 'todo/delete_form.html'
#    
#    def get_success_url(self):
#        return self.get_object().get_relate_task_url()
