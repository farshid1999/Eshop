from django.urls import path
from .views import ArticlesView,ArticleDetailView
urlpatterns=[
    path('',ArticlesView.as_view(),name='articles_page'),
    path('cat/<str:category>', ArticlesView.as_view(), name='articles_by_category_list'),
    path('<pk>', ArticleDetailView.as_view(), name='articles_detail'),
]
