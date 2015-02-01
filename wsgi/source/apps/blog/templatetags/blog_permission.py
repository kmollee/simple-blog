from django.template import Library

register = Library()


@register.filter(name='has_perm')
def has_perm(object, user):
    return object.is_owner(user) or user.is_superuser
