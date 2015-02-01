from django.conf import settings
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, login, logout, authenticate
)
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic import RedirectView, TemplateView, FormView, CreateView, UpdateView, DetailView
from .forms import LoginForm, UserCreationForm, ChangePassWordForm, ResetPasswordForm, SetPasswordForm
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.template import loader
from django.contrib.auth import get_user_model
from utils import mixins



def anonymous_required(func):
    def as_view(request, *args, **kwargs):
        redirect_to = kwargs.get('next', settings.LOGIN_REDIRECT_URL)
        if request.user.is_authenticated():
            return redirect(redirect_to)
        response = func(request, *args, **kwargs)
        return response
    return as_view


class IndexView(TemplateView):

    """ login_logout page"""
    template_name = 'account/index.html'


class LoginView(FormView):

    """login page"""
    form_class = LoginForm
    template_name = 'account/form.html'
    success_url = reverse_lazy('account:index')

    def form_valid(self, form):
        form.performLogin(self.request)
        messages.add_message(
            self.request, messages.SUCCESS, 'login success!')
        nextURL = self.request.GET.get('next')
        if nextURL:
            return HttpResponseRedirect(nextURL)
        else:
            return HttpResponseRedirect(self.get_success_url())

    @method_decorator(anonymous_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    # def form_invalid(self):
    #     messages.add_message(
    #         self.request, messages.ERROR, 'username or password is wrong')
    #     return HttpResponseRedirect(reverse_lazy('account:login'))
    def get_success_url(self):
        return self.success_url

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        #form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            print('form_invalid')
            return self.form_invalid(form)


class LogoutView(mixins.LoginRequiredMixin, RedirectView):

    """
    logout view need login
    """
    login_url = reverse_lazy('account:login')
    permanent = False
    query_string = True

    def get_redirect_url(self):
        logout(self.request)
        messages.add_message(self.request, messages.INFO, 'logout success!')
        return self.login_url


class CreateUser(CreateView):

    """
    register page
    """
    model = User
    template_name = 'account/form.html'
    success_url = reverse_lazy('account:index')
    form_class = UserCreationForm

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    @method_decorator(anonymous_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ChangePassWordView(FormView):
    form_class = ChangePassWordForm
    success_url = reverse_lazy('account:index')
    template_name = 'account/form.html'

    def form_valid(self, form):
        """
        if not form.check_old_password(self.request.user):
            messages.add_message(
                self.request, messages.ERROR, 'old password is not match')
            return super().form_invalid(form)
        """
        user = self.request.user
        user.set_password(form.cleaned_data['newpassword'])
        user.save()
        messages.add_message(self.request, messages.INFO, 'password changed')
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'request': self.request
        })
        return kwargs

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        #form = self.form_class(request.POST)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ResetPasswordRequestView(FormView):
    form_class = ResetPasswordForm
    success_url = reverse_lazy('account:login')
    template_name = 'account/form.html'

    def getUserFromEmail(self, email):
        return User.objects.get(email=email)
    def form_valid(self, form):
        userMail = form.cleaned_data.get('email')
        user = self.getUserFromEmail(userMail)
        print('email', user.email)

        c = {
            'email': user.email,
            'domain': self.request.META['HTTP_HOST'],
            'site_name': 'your site',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': default_token_generator.make_token(user),
            'protocol': 'http'
        }

        subject_template_name = 'account/password_reset_subject.txt'

        email_template_name = 'account/password_reset_email.html'

        subject = loader.render_to_string(subject_template_name, c)
        subject = ''.join(subject.splitlines())
        email = loader.render_to_string(email_template_name, c)
        send_mail(
            subject, email, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
        messages.success(self.request, 'An email has been sent to ' + user.email +
                         ". Please check its inbox to continue reseting password.")
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            messages.add_message(
                request, messages.ERROR, 'No user is associated with this email address')
            return self.get(request, *args, **kwargs)


class PasswordResetConfirmView(FormView):
    template_name = "account/form.html"
    success_url = reverse_lazy('account:login')
    form_class = SetPasswordForm

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
        """
        View that checks the hash in a password reset link and presents a
        form for entering a new password.
        """
        UserModel = get_user_model()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        assert uidb64 is not None and token is not None  # checked by URLconf
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password = form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password has been reset.')
                return self.form_valid(form)
            else:
                messages.error(
                    request, 'Password reset has not been unsuccessful.')
                return self.form_invalid(form)
        else:
            messages.error(
                request, 'The reset password link is no longer valid.')
            return self.form_invalid(form)
