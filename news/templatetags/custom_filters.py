import re

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

BAD_WORDS = ['редиска', 'хрен', 'дурак']  # Список нежелательных слов


@register.filter(name='censor')
@stringfilter  # Гарантирует, что фильтр применяется только к строкам
def censor(value):
    if not isinstance(value, str):
        raise TypeError("Фильтр 'censor' применяется только к строкам")

    for word in BAD_WORDS:
        # Ищем слова с любым регистром первой буквы
        pattern = r'\b{}\b'.format(word)
        replacement = word[0] + '*' * (len(word) - 1)
        value = re.sub(pattern, replacement, value, flags=re.IGNORECASE)

    return value