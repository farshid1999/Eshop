from django.db import models

# Create your models here.

class ContactUs(models.Model):
    title=models.CharField(max_length=300,verbose_name='عنوان')
    email=models.EmailField(max_length=300,verbose_name='ایمیل')
    fulname=models.CharField(max_length=300,verbose_name='نام و نام خانوادگی')
    message=models.TextField(verbose_name='متن کاربر')
    create_date=models.DateTimeField(verbose_name='تاریخ ایجاد متن',auto_now_add=True)
    response=models.TextField(verbose_name='پاسخ متن کاربر')
    is_reade_by_admin=models.BooleanField(verbose_name='فعال/غیر فعال')
    class Meta:
        verbose_name='تماس با ما'
        verbose_name_plural='لیست تماس با ما'

    def __str__(self):return self.title

class Profile(models.Model):
    image=models.ImageField(upload_to='images')
