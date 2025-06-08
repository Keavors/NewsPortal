from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
import models
from .models import Post, Author
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse
from .models import Category
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import TimezoneForm

@login_required
def set_timezone(request):
    if request.method == 'POST':
        form = TimezoneForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = TimezoneForm(instance=request.user)
    return render(request, 'users/timezone.html', {'form': form})

class ArticleDetailView(DetailView):
    model = Post
    template_name = 'articles/article_detail.html'
    context_object_name = 'article'

    @method_decorator(cache_page(300))  # 5 минут
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class ArticleList(ListView):
    model = Post
    template_name = 'articles/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(post_type='article').order_by('-created_at')

    @method_decorator(cache_page(300))  # 5 минут
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

@login_required
def subscribe_category(request, category_id):
    category = Category.objects.get(id=category_id)
    category.subscribers.add(request.user)
    return JsonResponse({'status': 'subscribed'})

@login_required
def unsubscribe_category(request, category_id):
    category = Category.objects.get(id=category_id)
    category.subscribers.remove(request.user)
    return JsonResponse({'status': 'unsubscribed'})

class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'news.change_post'
    model = Post
    template_name = 'news/post_edit.html'
    fields = ['title', 'text', 'categories']
@login_required
def become_author(request):
    author_group = Group.objects.get(name='authors')
    request.user.groups.add(author_group)
    return redirect('news_list')


class HomePage(TemplateView):
    template_name = 'flatpages/index.html'

    @method_decorator(cache_page(60))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class NewsList(ListView):
    model = Post
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    ordering = ['-created_at']
    paginate_by = 10  # Добавляем пагинацию к существующему коду

    def get_queryset(self):
        return Post.objects.filter(post_type='news').order_by('-created_at')

    @method_decorator(cache_page(300))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class NewsDetail(DetailView):
    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'news'

    @method_decorator(cache_page(300))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# Новые классы добавляем в конец файла
class PostSearch(ListView):
    model = Post
    template_name = 'news/post_search.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'news'
        return super().form_valid(form)


class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'article'
        return super().form_valid(form)


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('news_list')

from django.utils.translation import gettext_lazy as _

class Post(models.Model):
    title = models.CharField(_('Title'), max_length=200)
    text = models.TextField(_('Text'))

    def __str__(self):
        return _('Post: %(title)s') % {'title': self.title}