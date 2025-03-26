import django_filters
from .models import Post
from django import forms

class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Заголовок'
    )
    author__user__username = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Имя автора'
    )
    created_after = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gte',
        label='Дата (не ранее)',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = []