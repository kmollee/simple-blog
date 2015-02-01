from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Fieldset, Field, Button
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.conf import settings
from hashlib import sha1




class LoginForm(forms.Form):
    username = forms.CharField(label="username", max_length=25)
    password = forms.CharField(label="password", widget=forms.PasswordInput)
    remember = forms.BooleanField(required=False, widget=forms.CheckboxInput())

    def __init__(self, action='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'LoginForm'
        self.helper.form_method = 'POST'
        self.helper.form_action = action
        self.helper.layout = Layout(
            Fieldset(
                'Login',
                'username',
                'password',
                'remember'
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn-primary'),
                Button('cancel', 'Cancel', css_class='button',
                       onclick="parent.history.back();")
            )
        )

    def check(self, username, password):
        return authenticate(username=username, password=password)

    def performLogin(self, request):
        # get form field data
        cleaned_data = self.cleaned_data
        # print(cleaned_data)
        username = cleaned_data['username']
        password = cleaned_data['password']
        # use form field data get the user object
        user = self.check(username, password)
        # login request, as user
        login(request, user)
        # check setting is set session remeber is open?
        # True or False, or None(not setting)
        #remember = settings.SESSION_REMEMBER
        session_age = getattr(settings, 'SESSION_REMEMBER', None)
        remember = cleaned_data.get('remember', None)
        # if remember function is open, set session expire
        if remember:
            request.session.set_expiry(settings.SESSION_COOKIE_AGE)
        else:
            request.session.set_expiry(0)

    def clean(self):
        # get field data
        cleaned_data = self.cleaned_data
        # print(cleaned_data)
        username = cleaned_data.get('username', '')
        password = cleaned_data.get('password', '')
        if username == '' or password == '':
            raise forms.ValidationError(
                'Username or Passoword should not be blank.')
        # check username is exist in system
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError(
                'Username "%s" is not exist in system.' % username)
        # there step, username is confirm exist in system
        # try use form field data, get user object
        # if pass, return user obj, not pass, return None
        user_obj = self.check(username, password)
        if user_obj:
            return cleaned_data
        else:
            raise forms.ValidationError('Username or Password is not correct.')
class UserCreationForm(UserCreationForm):
    email = forms.EmailField(label="E-mail", required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user

    def __init__(self, action='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'UserCreationForm'
        self.helper.form_method = 'POST'
        self.helper.form_action = action
        self.helper.layout = Layout(
            Fieldset(
                'Register',
                'username',
                'email',
                'password1',
                'password2'
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn-primary'),
                Button('cancel', 'Cancel', css_class='button',
                       onclick="parent.history.back();")
            )
        )


class ChangePassWordForm(forms.Form):
    oldpassword = forms.CharField(
        label="old password", widget=forms.PasswordInput)
    newpassword = forms.CharField(
        label="new password", widget=forms.PasswordInput)
    confirm = forms.CharField(
        label="confirm password", widget=forms.PasswordInput)

    # add request, convinice to get current request user
    def __init__(self, request=None, action='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.helper = FormHelper()
        self.helper.form_id = 'ChangePassWordForm'
        self.helper.form_method = 'POST'
        self.helper.form_action = action
        self.helper.layout = Layout(
            Fieldset(
                'Change Password',
                'oldpassword',
                'newpassword',
                'confirm'
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn-primary'),
                Button('cancel', 'Cancel', css_class='button',
                       onclick="parent.history.back();")
            )
        )

    def clean_oldpassword(self):
        user = self.request.user
        old_password = self.cleaned_data.get('oldpassword')
        # check old password is match login user password
        auth_user = authenticate(username=user.username, password=old_password)
        """
        print(user.password)
        print(user.password.split('$'))
        _, salt, hashpw = user.password.split('$')
        return sha1(salt + old_password).hexdigest() == hashpw
        """
        # is auth is pass, will return user object
        if auth_user:
            return True
        else:
            raise forms.ValidationError("old password is not match.")
            return False

    def clean(self):
        cleaned_data = self.cleaned_data
        # get new password
        password1 = cleaned_data.get('newpassword')
        # get mini password len, if setting is not set, set to 6
        min_len = getattr(settings, "PASSWORD_MINIMUM_LENGHT", 6)
        # if new password length is not larger or equal, raise valid error
        if len(password1) < min_len:
            raise forms.ValidationError(
                "Password too short! minimum length is " + " [%d]" % min_len)

        #password1 = cleaned_data.get('newpassword')
        # get password confirm
        password2 = cleaned_data.get('confirm')
        # check two new password is match
        if password1 != password2:
            raise forms.ValidationError(
                "The two password fields didn't match.")
        return cleaned_data


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(label="Email address")

    def __init__(self, action='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'ResetPasswordForm'
        self.helper.form_method = 'POST'
        self.helper.form_action = action
        self.helper.layout = Layout(
            Fieldset(
                'Forget Password?',
                'email',
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn-primary'),
                Button('cancel', 'Cancel', css_class='button',
                       onclick="parent.history.back();")
            )
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        '''
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError(
                'this email is not exist in system.' % email)
        '''
        if User.objects.filter(email=email).exists():
            return email
        else:
            raise forms.ValidationError(
                'this email is not exist in system.' % email)


class SetPasswordForm(forms.Form):

    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    new_password1 = forms.CharField(label=("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=("New password confirmation"),
                                    widget=forms.PasswordInput)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'])
        return password2

    def __init__(self, action='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'SetPasswordForm'
        self.helper.form_method = 'POST'
        self.helper.form_action = action
        self.helper.layout = Layout(
            Fieldset(
                'Reset Password',
                'new_password1',
                'new_password2',
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn-primary'),
                Button('cancel', 'Cancel', css_class='button',
                       onclick="parent.history.back();")
            )
        )
