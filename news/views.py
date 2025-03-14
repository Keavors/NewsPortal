from django.views.generic import ListView, DetailView
from .models import Post
from django.views.generic import TemplateView

class HomePage(TemplateView):
    template_name = 'flatpages/index.html'

class NewsList(ListView):
    model = Post
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    ordering = ['-created_at']  # Сортировка от новых к старым
    paginate_by = 10  # Опционально: пагинация

    def get_queryset(self):
        return Post.objects.filter(post_type='news').order_by('-created_at')

class NewsDetail(DetailView):
    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'news'