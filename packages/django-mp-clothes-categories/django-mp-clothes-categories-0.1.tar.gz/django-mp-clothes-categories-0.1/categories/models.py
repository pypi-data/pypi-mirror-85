
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from slugify import slugify_url
from ordered_model.models import OrderedModel
from assets.images.models import LogoField

from categories.constants import SEX_CHOICES


class ParentCategory(OrderedModel):

    name = models.CharField(_('Category name'), max_length=255)

    def get_absolute_url(self):
        return reverse('products:parent-category', kwargs={
            'slug': slugify_url(self.name, separator='_'),
            'pk': self.pk
        })

    def __str__(self):
        return self.name

    class Meta(OrderedModel.Meta):
        verbose_name = _('Parent category')
        verbose_name_plural = _('Parent categories')


class Category(OrderedModel):

    parent = models.ForeignKey(
        ParentCategory,
        verbose_name=_('Parent category'),
        on_delete=models.CASCADE,
        related_name='children',
        blank=True, null=True)

    name = models.CharField(_('Category name'), max_length=255)

    item_name = models.CharField(
        _('Item name'), max_length=255, blank=True)

    logo = LogoField(upload_to='categories', editable=True)

    description = models.TextField(
        _('Description'), blank=True, null=True, max_length=8192)

    grid = models.TextField(
        _('Size grid'), blank=True, null=True, max_length=4096)

    sex = models.PositiveSmallIntegerField(
        _('Sex'), choices=SEX_CHOICES, null=True, blank=True)

    age = models.CharField(_('Age'), max_length=100, blank=True, choices=(
        ('adult', _('Adult')),
        ('child', _('Child'))
    ))

    order_with_respect_to = 'parent'

    @property
    def slug(self):
        return slugify_url(self.name, separator='_')

    def __str__(self):
        if self.parent:
            return '{} / {}'.format(self.parent.name, self.name)

        return self.name

    def get_absolute_url(self):

        if self.parent:
            return reverse('products:child-category', kwargs={
                'parent_slug': slugify_url(self.parent.name, separator='_'),
                'parent_pk': self.parent.pk,
                'slug': self.slug,
                'pk': self.pk
            })

        return reverse('products:category', kwargs={
            'slug': self.slug,
            'pk': self.pk
        })

    class Meta(OrderedModel.Meta):
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class CategoryField(models.ForeignKey):

    def __init__(
            self,
            to='categories.Category',
            verbose_name=_('Category'),
            on_delete=models.CASCADE,
            *args, **kwargs):

        super(CategoryField, self).__init__(
            to,
            verbose_name=verbose_name,
            on_delete=on_delete,
            *args, **kwargs)
