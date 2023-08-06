
from django import template
from django.apps import apps


register = template.Library()


@register.simple_tag
def get_parent_categories():
    return apps.get_model('categories', 'ParentCategory').objects.all()\
        .prefetch_related('children')


@register.simple_tag
def get_categories_without_parent():
    return apps.get_model('categories', 'Category').objects.filter(
        parent__isnull=True)
