from django.urls import path
from django.urls import include
from .views import (
    NewsList, NewsDetail, PostSearch,
    NewsCreate, ArticleCreate, PostUpdate, PostDelete, become_author, subscribe_category, unsubscribe_category,
    ArticleDetailView, ArticleList
)

urlpatterns = [
    # Основные URL
    path('', NewsList.as_view(), name='news_list'),
    path('<int:pk>/', NewsDetail.as_view(), name='news_detail'),
    path('search/', PostSearch.as_view(), name='post_search'),

    # Новости
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='news_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),

    # Статьи
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='article_delete'),

    path('become-author/', become_author, name='become_author'),

    path('category/<int:category_id>/subscribe/', subscribe_category, name='subscribe_category'),
    path('category/<int:category_id>/unsubscribe/', unsubscribe_category, name='unsubscribe_category'),

    path('accounts/', include('allauth.urls')),
    path('articles/', ArticleList.as_view(), name='article_list'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
]
