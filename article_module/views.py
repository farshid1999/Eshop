from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic import DetailView
from .models import Article,ArticleCategory,ArticleComments
from .forms import ArticleCommentsModelForm
# Create your views here.


class ArticlesView(ListView):
    template_name = 'article_module/article_page.html'
    model = Article
    paginate_by = 3
    context_object_name = 'articles'

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True)
        category_name = self.kwargs.get("category")
        if category_name:
            queryset = queryset.filter(selected_category__url_title__exact=category_name)

        return queryset


class ArticleDetailView(DetailView):
    template_name = 'article_module/article_detail.html'
    model = Article


    def get_queryset(self):
        query=super().get_queryset().filter(is_active=True)
        return query

    def get_context_data(self,*args,**kwargs):
        context=super(ArticleDetailView,self).get_context_data(**kwargs)
        article_id = self.kwargs.get('pk')

        current_article = Article.objects.get(id=article_id)
        previous_article = Article.objects.filter(id__lt=current_article.id, is_active=True).order_by('-id').first()
        next_article = Article.objects.filter(id__gt=current_article.id, is_active=True).order_by('id').first()

        categories = ArticleCategory.objects.raw(
            """
            SELECT *
            FROM article_module_articlecategory amac
            INNER JOIN article_module_article_selected_category amasc 
                ON amac.id = amasc.articlecategory_id
            INNER JOIN article_module_article ama 
                ON ama.id = amasc.article_id
            WHERE ama.id = %s
            order by amac.id ASC
            """, article_id
        )
        # amac.parent_id is NULL and
        context['current_article'] = current_article
        context["previous_article"] = previous_article
        context["next_article"] = next_article
        context["categories"] = categories
        context["comments"]=ArticleComments.objects.filter(article_id=current_article.id,is_active=True,parent=None).order_by("-id").prefetch_related("articlecomments_set")
        context["comments_count"]=ArticleComments.objects.filter(article_id=current_article.id,is_active=True).count()
        context["form"]=ArticleCommentsModelForm

        return context

    def post(self,request,*args,**kwargs):
        article_id=self.kwargs.get("pk")
        current_article = Article.objects.get(id=article_id)

        form=ArticleCommentsModelForm(request.POST)
        if form.is_valid():

            comment = form.save(commit=False)
            comment.article = current_article
            comment.user = request.user
            comment.save()

        return redirect('articles_detail', pk=article_id)




def article_categories_component(request:HttpRequest):
    article_main_category=ArticleCategory.objects.filter(is_active=True,parent_id=None)
    context={
        'main_categoties': article_main_category
    }
    return render(request,'article_module/component/article_categories_component.html',context)


