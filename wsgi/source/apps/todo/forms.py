from __future__ import absolute_import
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Fieldset, Field, Button
from . import models


def clean_unique(form, field, exclude_initial=True, 
                 format="The %(field)s %(value)s has already been taken."):
    value = form.cleaned_data.get(field)
    if value:
        qs = form._meta.model._default_manager.filter(**{field:value})
        if exclude_initial and form.initial:
            initial_value = form.initial.get(field)
            qs = qs.exclude(**{field:initial_value})
        if qs.count() > 0:
            raise forms.ValidationError(format % {'field':field, 'value':value})
    return value
class ListForm(forms.ModelForm):
    class Meta:
        fields = ('name',)
        model = models.List

    def __init__(self, action='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'ListForm'
        self.helper.form_method = 'POST'
        #self.helper.form_class = 'form-inline'
        self.helper.form_action = action
        self.helper.layout = Layout(
            Fieldset(
                'List Form',
                'name',
            ),
            Submit('submit', 'Submit', css_class='btn-primary'),
            Button('cancel', 'Cancel', css_class='button',
                       onclick="parent.history.back();")
            #ButtonHolder(
            #    Submit('submit', 'Submit', css_class='btn-primary'),
            #    Button('cancel', 'Cancel', css_class='button',
            #           onclick="parent.history.back();")
            #)
        )

    def save(self, submitter=None, *args, **kwargs):
        if not self.instance.id:
            self.instance.author = submitter
        return super().save()


class ItemForm(forms.ModelForm):
    class Meta:
        fields = ('title', 'note', 'priority')
        model = models.Item
    def __init__(self, action='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        # due_date = forms.DateField(
        #     required=False,
        #     widget=forms.DateTimeInput(attrs={'class': 'due_date_picker'})
        # )
        note = forms.CharField(widget=forms.Textarea())
        self.helper = FormHelper()
        self.helper.form_id = 'ItemForm'
        self.helper.form_method = 'POST'
        self.helper.form_action = action
        self.helper.layout = Layout(
            Fieldset(
                'Item',
                'title',
                'note',
                'priority'
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn-primary'),
                Button('cancel', 'Cancel', css_class='button',
                       onclick="parent.history.back();")
            )
        )
    def save(self, list_obj=None, submitter=None, *args, **kwargs):
        if not self.instance.id:
            self.instance.created_by = submitter
        if list_obj:
            self.instance.list = list_obj
        return super().save()


