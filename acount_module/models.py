from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser
from django.apps import apps

# Create your models here.


class User(AbstractUser):
    mobile = models.CharField(max_length=20, verbose_name="Mobile", null=True, blank=True)
    email_active_code = models.CharField(max_length=100, verbose_name="Email Activation Code", blank=True)
    about_user = models.TextField(null=True, blank=True, verbose_name='About User')
    avatar = models.ImageField(upload_to='images/user_avatar', verbose_name='User Avatar', null=True, blank=True)
    address = models.TextField(blank=True, null=True, verbose_name="Address")
    favorite = models.ManyToManyField('product_model.Product', blank=True, related_name=("userfavorites"),
                                      verbose_name="Favorites")
    def get_favorite_product(self):
        Product = apps.get_model('product_model', 'Product')
        return Product.objects.all()

    class Meta:
        verbose_name="کاربر"
        verbose_name_plural="کاربران"

    def __str__(self):
        if self.first_name and self.last_name:
            return self.get_full_name()
        else:
            return self.email


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    province = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    detail = models.TextField()

    def __str__(self):
        return f"{self.province} - {self.city}"