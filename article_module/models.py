from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from acount_module.models import User
import jdatetime
import re
# Create your models here.



class ArticleCategory(models.Model):
    parent=models.ForeignKey('ArticleCategory',on_delete=models.CASCADE,verbose_name='دسته بندی والد',null=True,blank=True)
    title=models.CharField(verbose_name='عنوان دسته بندی',max_length=200)
    url_title=models.CharField(max_length=200,unique=True,verbose_name='عنوان در url')
    is_active=models.BooleanField(default=True,verbose_name='فعال/غیر فعال')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name='دسته بندی مقاله'
        verbose_name_plural='دسته بندی های مقاله '

def get_default_date_now():
    now = timezone.localtime(timezone.now())
    return jdatetime.date.fromgregorian(date=now.date())

def get_default_time_now():
    now = timezone.localtime(timezone.now())
    return jdatetime.time.fromisoformat(str(now.time()))

class Article(models.Model):

    title=models.CharField(max_length=500,verbose_name='عنوان مقاله')
    slug=models.SlugField(null=False,blank=True,max_length=500,unique=True,db_index=True,allow_unicode=True,verbose_name='عنوان در url')
    image=models.ImageField(verbose_name='تصویر مقاله',upload_to='images/articles')
    short_description=models.TextField(verbose_name='توضیحات کوتاه')
    text=models.TextField(verbose_name='متن مقاله')
    is_active=models.BooleanField(verbose_name='فعال/غیر فعال',default=True)
    selected_category=models.ManyToManyField(ArticleCategory,verbose_name='دسته بندی ها')
    create_time=models.TimeField(verbose_name='زمان مقاله',default=get_default_time_now)
    create_date=models.DateField(verbose_name='تاریخ مقاله',default=get_default_date_now)
    author=models.ForeignKey(User,verbose_name='نویسنده',on_delete=models.CASCADE,null=True,editable=False)


    def save(self, *args, **kwargs):
        self.slug = self.generate_slug(self.title)
        super().save(*args, **kwargs)

    def generate_slug(self, title):
        sentence=[]
        sentence=title.split(' ')
        title_slug='-'.join(sentence)
        return title_slug


    def __str__(self):
        return self.title

    class Meta:
        verbose_name='مقاله'
        verbose_name_plural='مقالات'


class ArticleComments(models.Model):
    article=models.ForeignKey(Article,on_delete=models.CASCADE,verbose_name='مقاله')
    parent=models.ForeignKey("ArticleComments",on_delete=models.CASCADE,verbose_name="والد",blank=True,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="کاربر")
    text=models.TextField(verbose_name="متن")

    is_active=models.BooleanField(default=False,verbose_name="فعال/غیر فعال")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name='کامنت'
        verbose_name_plural='کامنت ها'
