#@+leo-ver=5-thin
#@+node:lee.20150101103558.63: * @file mixins.py
#@@language python
#@@tabwidth -4
#@+<<declarations>>
#@+node:lee.20150101103558.64: ** <<declarations>>
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages
from .ajax import login_required_ajax
from .django_remote_forms.forms import RemoteForm 
import json
from django.http import HttpResponse
from .decorators import my_login_required
from django.http import JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.query import QuerySet
from django.core.paginator import Paginator, QuerySetPaginator, Page, InvalidPage
from .paginator import DiggPaginator
from django.http import Http404
#@-<<declarations>>


#@+others
#@+node:lee.20150101103558.65: ** class LoginRequiredMixin
class LoginRequiredMixin(object):
    #@+others
    #@+node:lee.20150101103558.66: *3* dispatch
    @method_decorator(my_login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


    #@-others
#@+node:lee.20150101103558.73: ** class SuperUserCheckMixin
class SuperUserCheckMixin(object):

    """
    check object can do permission
    only user is super user or object's owner
    if pass: go on
    if fail: redirect to fail path
    """
    # http://jsatt.com/blog/decorators-vs-mixins-for-django-class-based-views/
    user_check_failure_path = None
    
    #@+others
    #@+node:lee.20150101103558.74: *3* check_user
    def check_user(self, user):
        # check user is object's owner or user is super user
        return user.is_superuser


    #@+node:lee.20150101103558.69: *3* user_check_failed
    def user_check_failed(self, request, *args, **kwargs):
        # if check fail, redirect to fail path
        return redirect(self.user_check_failure_path)

    #@+node:lee.20150101103558.70: *3* dispatch
    @method_decorator(my_login_required)
    def dispatch(self, request, *args, **kwargs):
        # check permission
        if not self.check_user(request.user):
            if request.is_ajax():
                return HttpResponse(status=403)
            # set error message
            messages.error(
                    request,
                    'You do not have the permission required to perform the '
                    'requested operation.')
            # if has set check fail path, redirect to that path
            if self.user_check_failure_path:
                return self.user_check_failed()
            # else raise 403
            raise PermissionDenied()
        # if pass, go on
        return super().dispatch(request, *args, **kwargs)


    #@-others
#@+node:lee.20150101103558.67: ** class OwnerOrSuperuserMixin
class OwnerOrSuperuserMixin(SuperUserCheckMixin):

    #@+others
    #@+node:lee.20150101103558.68: *3* check_user
    def check_user(self, user):
        # check user is object's owner or user is super user
        return self.get_object().is_owner(user) or user.is_superuser

    #@-others
#@+node:lee.20150101103558.77: ** PermissionsRequiredMixin
class PermissionsRequiredMixin(object):
    """
    View mixin which verifies that the logged in user has the specified
    permissions.

    Settings:

    `required_permissions` - list/tuple of required permissions

    Example Usage:

        class SomeView(PermissionsRequiredMixin, ListView):
            ...
            required_permissions = (
                'app1.permission_a',
                'app2.permission_b',
            )
            ...
    """
    required_permissions = ()

    @method_decorator(my_login_required)
    def dispatch(self, request, *args, **kwargs):
        # check permission_required tuple is set properly
        # if 
        if self.permission_required:
            raise ImproperlyConfigured("'PermissionRequiredMixin' requires "
                "'permission_required' attribute to be set.")
        if not request.user.has_perms(self.required_permissions):
            if request.is_ajax():
                return HttpResponse(status=403)
            messages.error(
                request,
                'You do not have the permission required to perform the '
                'requested operation.')
            return PermissionDenied()
        return super(PermissionsRequiredMixin, self).dispatch(
            request, *args, **kwargs)
#@+node:lee.20150101103558.78: ** StaffRequiredMixin
class StaffRequiredMixin(object):
    """
    View mixin which requires that the authenticated user is a staff member
    (i.e. `is_staff` is True).
    """

    @method_decorator(my_login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            if request.is_ajax():
                return HttpResponse(status=403)
            messages.error(
                request,
                'You do not have the permission required to perform the '
                'requested operation.')
            return PermissionDenied()
        return super().dispatch(request, *args, **kwargs)
#@+node:lee.20150101103558.97: ** RequireSignInAjax
class RequireSignInAjax(object):
    @method_decorator(login_required_ajax())
    def dispatch(self, request, *args, **kwargs):
        return super(RequireSignInAjax, self).dispatch(request, *args, **kwargs) 
#@+node:lee.20150101103558.98: ** JSONResponseMixin
class JSONResponseMixin(object):

    # a mixin that can be used to render a JSON response
    response_class = HttpResponse

    def render_to_response(self, context, **response_kwargs):
        # returns a JSON response, transforming 'context' to make the payload
        response_kwargs['content_type'] = 'application/json'
        return self.response_class(self.convert_context_to_json(context), **response_kwargs)

    def convert_context_to_json(self, context):
        # this would need to be a bit more complex if we're dealing with more complicated variables
        return json.dumps(context)
#@+node:lee.20150101103558.100: ** AjaxableResponseMixin
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
                'pk': self.get_object().pk,
            }
            return JsonResponse(data)
        else:
            return response
#@+node:lee.20150110150203.2: ** HybridResponseMixin
class HybridResponseMixin(object):

    def get_data(self, context):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """
        # only return object or object_list
        # other context will ignore
        data = dict()
        
        
        #check method is defined in model
        if "serialize_field" not in dir(self.model):
            raise NotImplementedError('model has not serialize_field method, fix it!')
        
        # use in listview
        if 'object_list' in context:
            tmp = [_i for _i in context['object_list']]
            data['object_list'] = serializers.serialize("json", tmp, fields=self.model.serialize_field())
        # use in single object view
        if 'object' in context:
            data['object'] = serializers.serialize("json", [context['object']],  fields=self.model.serialize_field())
        return json.dumps(data, cls=DjangoJSONEncoder)

    def get_object_data(self, context):
        if 'object_list' in context:
            return context['object_list']
        return {context['object']}
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return HttpResponse(self.get_data(context), content_type="application/json", **response_kwargs)

    def render_to_response(self, context):
        # if request is ajax
        if self.request.is_ajax():
            # also check request data type
            # default is html, use output as parameter
            # like update?output=html
            if self.request.GET.get('output', 'html') == 'html':
                return super(HybridResponseMixin, self).render_to_response(context)
            # if output is json
            return self.render_to_json_response(context)
        else:
            return super(HybridResponseMixin, self).render_to_response(context)
#@+node:lee.20150110150203.3: ** HybridFormResponseMixin
class HybridFormResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return super(HybridFormResponseMixin, self).form_invalid(form)


    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return super(HybridFormResponseMixin, self).form_valid(form)
#@+node:lee.20150113193020.13: ** PaginatorMixin
class PaginatorMixin(object):
    """
    refer
    https://bitbucket.org/dicos/digg-like-paginator/src/8cd1de9da5e5?at=master - this one adapt python34
    and
    https://djangosnippets.org/snippets/773/
    use in ListView, source code in utils
    """
    paginator_class = DiggPaginator
    paginate_by = 10
    # paginator content body
    paginator_body = 5
    # paginator left or right tail
    paginator_tail = 2
    
    #@+others
    #@+node:lee.20150113193020.14: *3* def get_paginator
    def get_paginator(self, queryset, per_page, orphans=0, allow_empty_first_page=True, body=5, tail=2):
        """
        Return an instance of the paginator for this view.
        """
        return self.paginator_class(queryset, per_page, body=body, tail=tail, orphans=orphans, allow_empty_first_page=allow_empty_first_page)
    #@+node:lee.20150113193020.15: *3* def paginate_queryset
    def paginate_queryset(self, queryset, page_size):
        """
        Paginate the queryset, if needed.
        """
        paginator = self.get_paginator(queryset, page_size, allow_empty_first_page=self.get_allow_empty(), body=self.paginator_body, tail=self.paginator_tail)
        page = self.kwargs.get('page') or self.request.GET.get('page') or 1
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                raise Http404("Page is not 'last', nor can it be converted to an int.")
        try:
            page = paginator.page(page_number)
            return (paginator, page, page.object_list, page.has_other_pages())
        except InvalidPage:
            raise Http404('Invalid page (%(page_number)s)' % {'page_number': page_number })
    #@-others
#@-others
#@-leo
