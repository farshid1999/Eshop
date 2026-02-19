from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.urls import reverse
from django.utils.text import slugify
from acount_module.models import User
from jalali_date import date2jalali,datetime2jalali,to_current_timezone
from datetime import datetime
# Create your models here.



class ProductCatogory(models.Model):
    parent=models.ForeignKey("ProductCatogory",verbose_name="والد",blank=True,null=True,on_delete=models.CASCADE)
    title=models.CharField(max_length=300,db_index=True,verbose_name='عنوان')
    url_title=models.CharField(max_length=300,db_index=True,verbose_name='عنوان در url',null=True,blank=True)
    is_active=models.BooleanField(verbose_name="فعال/غیر فعال")
    is_delete=models.BooleanField(verbose_name="حذف شده/نشده")

    def save(self, *args, **kwargs):
        self.url_title = self.generate_slug(self.title)
        super().save(*args, **kwargs)

    def generate_slug(self, title):
        sentence=[]
        sentence=title.split(' ')
        title_slug='-'.join(sentence)
        return title_slug

    class Meta:
        verbose_name="دسته بندی ها"
        verbose_name_plural="دسته بندی"

    def __str__(self):return f"{self.title}-{self.url_title}"

class PruductBrand(models.Model):
    title=models.CharField(max_length=300,db_index=True,verbose_name='نام برند')
    url_title=models.CharField(default='',max_length=300,db_index=True,verbose_name='عنوان در url')
    is_active=models.BooleanField(verbose_name='فعال/غیر فعال')

    class Meta:
        verbose_name='برند'
        verbose_name_plural='برند ها'
    def __str__(self):return self.title

class Product(models.Model):
    title = models.CharField(max_length=500, verbose_name="Product Title")
    image = models.ImageField(upload_to="images", blank=True, null=True)
    category = models.ManyToManyField(ProductCatogory, related_name="product_categories", verbose_name='Categories')
    brand = models.ForeignKey(PruductBrand, verbose_name='Brand', on_delete=models.CASCADE, null=True, blank=True)
    price = models.IntegerField(verbose_name="Price")
    short_description = models.CharField(max_length=360, null=True, db_index=True, verbose_name="Short Description")
    description = models.TextField(verbose_name="Description", db_index=True)
    is_active = models.BooleanField(default=False, verbose_name="Active/Inactive")
    slug = models.SlugField(max_length=500, default="", null=False, db_index=True, blank=True, unique=True, verbose_name="URL Title")
    is_delete = models.BooleanField(verbose_name="Deleted/Not Deleted")

    def save(self, *args, **kwargs):
        self.slug = self.generate_slug(self.title)
        super().save(*args, **kwargs)

    def generate_slug(self, title):
        sentence=[]
        sentence=title.split(' ')
        title_slug='-'.join(sentence)
        return title_slug

    def __str__(self):return self.title

    def get_absolute_url(self):
        return reverse('detail_list',args=[self.slug])

    class Meta:
        verbose_name="محصول"
        verbose_name_plural="محصولات"


class SampleProductImages(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name="محصول مورد نظر")
    image=models.ImageField(upload_to="images/product_images",blank=True,null=True)
    is_active=models.BooleanField(default=True,verbose_name="فعال/غیر فعال")

    class Meta:
        verbose_name="عکس نمونه های محصول"
        verbose_name_plural="عکس های نمونه های محصولات"

class ProductTag(models.Model):
   caption=models.CharField(max_length=300,db_index=True,verbose_name='عنوان محصول')
   product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_tags")
   def __str__(self): return self.caption

   class Meta:
    verbose_name="تگ محصول"
    verbose_name_plural="تگ محصولات"


class VisitedProduct(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name="محصول بازدید شده")
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="کاربر بازدید کننده",null=True,blank=True)
    ip=models.CharField(verbose_name="آی پی کاربر")

    def __str__(self):return f"{self.product.title}/{self.ip}"

    class Meta:
        verbose_name="بازدید محصول"
        verbose_name_plural="بازدید های محصول"


def generate_date():
    now = datetime.now()
    jalali = date2jalali(now)
    return f"{jalali.year}-{str(jalali.month).zfill(2)}-{str(jalali.day).zfill(2)}"

def generate_time():
    now = datetime.now()
    return now.strftime("%H:%M:%S")

class CommentsProduct(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="کاربر")
    product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name="محصول")
    comment=models.TextField(verbose_name="دیدگاه")
    date=models.DateField(blank=True,null=True,default=generate_date,verbose_name="تاریخ")
    time = models.TimeField(blank=True, null=True, default=generate_time,verbose_name="زمان")

    def __str__(self): return f"{self.user} - {self.product}"

    class Meta:
        verbose_name="دیدگاه برای محصول"
        verbose_name_plural="دیدگاه ها برای محصولات"



