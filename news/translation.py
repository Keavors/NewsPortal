# news/translation.py
from modeltranslation.translator import register, TranslationOptions
from .models import Post, Category

@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'text')  # Поля для перевода

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)  # Поле для перевода