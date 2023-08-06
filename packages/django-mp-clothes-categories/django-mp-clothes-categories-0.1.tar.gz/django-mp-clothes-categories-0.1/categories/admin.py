
from django.db import models
from django.contrib import admin

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ordered_model.admin import OrderedModelAdmin
from modeltranslation.admin import TranslationAdmin
from modeltranslation.utils import get_translation_fields

from categories.models import Category, ParentCategory


@admin.register(Category)
class CategoryAdmin(OrderedModelAdmin, TranslationAdmin):

    list_display = [
        'id', 'name', 'parent', 'item_name', 'sex', 'age', 'move_up_down_links'
    ]

    list_display_links = ['id', 'name']

    list_filter = ['parent']

    fields = [
        'parent',
        tuple(get_translation_fields('name')),
        tuple(get_translation_fields('item_name')),
        ('logo', 'sex', 'age'),
        'grid',
        'description'
    ]

    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget}
    }


@admin.register(ParentCategory)
class ParentCategoryAdmin(OrderedModelAdmin, TranslationAdmin):

    list_display = ['name', 'move_up_down_links']
