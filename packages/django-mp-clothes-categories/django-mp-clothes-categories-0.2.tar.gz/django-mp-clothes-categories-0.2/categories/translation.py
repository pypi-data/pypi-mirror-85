
from modeltranslation.translator import translator

from categories.models import Category, ParentCategory


translator.register(ParentCategory, fields=['name'])
translator.register(Category, fields=['name', 'item_name', 'description'])
