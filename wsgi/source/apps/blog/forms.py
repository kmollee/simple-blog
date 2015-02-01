from __future__ import absolute_import
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Fieldset, Field, Button, Div
from .models import Entry, Tag, Comment
from pagedown.widgets import AdminPagedownWidget
from crispy_forms.bootstrap import FormActions


class EntryForm(forms.ModelForm):
    description = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        fields = ('title', 'description', 'tag')
        model = Entry

    def __init__(self, action='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'EntryForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-8'
        self.helper.form_action = action
        self.helper.layout = Layout(
            Fieldset(
                'Entry',
                'title',
                'description',
                'tag',
            ),
            FormActions(
                Submit('submit', 'Submit', css_class="btn-primary"),
                Button('cancel', 'Cancel', onclick='history.go(-1);')
            )
        )

    def save(self, submitter=None, *args, **kwargs):
        if not self.instance.pk:
            self.instance.submitter = submitter
        return super().save()


class CommentForm(forms.ModelForm):
    description = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = Comment
        fields = ('title', 'description')

    def __init__(self, title=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'CommentForm'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-8'
        self.helper.form_method = 'POST'
        self.fields['title'].initial = title
        self.helper.layout = Layout(
            Fieldset(
                'Comment',
                'title',
                'description',
            ),
            FormActions(
                Submit('submit', 'Submit', css_class="btn-primary"),
                Button('cancel', 'Cancel', onclick='history.go(-1);')
            )
        )

    def save(self, entry=None, submitter=None, *args, **kwargs):
        if not self.instance.pk:
            self.instance.entry = entry
            self.instance.submitter = submitter
        return super().save(*args, **kwargs)


class TagForm(forms.ModelForm):

    class Meta:
        fields = ('title',)
        model = Tag

    def __init__(self, action='', *args, **kwargs):
        super(TagForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'TagForm'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-8'
        self.helper.form_method = 'POST'
        self.helper.form_action = action
        self.helper.layout = Layout(
            Fieldset(
                'Tag',
                'title',
            ),
            FormActions(
                Submit('submit', 'Submit', css_class="btn-primary"),
                Button('cancel', 'Cancel', onclick='history.go(-1);')
            )
        )


class SearchForm(forms.Form):
    q = forms.CharField(label='Search', max_length=50)

    def __init__(self, q=None, action=None, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['q'].initial = q
        self.helper = FormHelper(self)
        self.helper.form_id = 'SearchForm'
        self.helper.form_class = 'searchform form-inline'
        self.helper.label_class = 'col-sm-3'
        self.helper.field_class = 'col-sm-8'
        self.helper.form_method = 'GET'
        self.helper.form_action = action
        #self.helper.template = 'bootstrap/table_inline_formset.html'

        #self.helper.add_input(Submit('submit', 'Submit'))
        # self.helper.layout = Layout(
        #    Field('q',),
        #)
