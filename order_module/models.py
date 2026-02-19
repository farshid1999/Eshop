from django.db import models
from acount_module.models import User
from product_model.models import Product
# Create your models here.

class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="کاربر")
    is_paid=models.BooleanField(verbose_name="پرداخت شده/نشده")
    payment_date=models.DateTimeField(blank=True,null=True,verbose_name="تاریخ پرداخت")

    def __str__(self):
        return f"{self.user.get_full_name()}"

    def calculate_total_price(self):
        total_amount=0
        if self.is_paid:
            for order_detail in self.orderdetail_set.all():
                total_amount+=order_detail.final_price *order_detail.count
        else:
            for order_detail in self.orderdetail_set.all():
                total_amount+=order_detail.final_price *order_detail.count
        return total_amount


    class Meta:
        verbose_name="سبد خرید"
        verbose_name_plural="سبد های خرید"

class Discount(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='کاربر')
    is_used=models.BooleanField(verbose_name='استفاده شده/نشده')
    is_active=models.BooleanField(verbose_name='فعال/غیر فعال',default=True)
    discount_code=models.CharField(verbose_name='کد تخفیف',max_length=20,unique=True,null=True,blank=True)
    discount_price=models.IntegerField(verbose_name='مقدار تخفیف',null=True,blank=True)
    expiration_date = models.DateTimeField(verbose_name='تاریخ انقضا', null=True, blank=True)

    def __str__(self):
        return f'{self.user.get_full_name()}'

    class Meta:
        verbose_name="کد تخفیف"
        verbose_name_plural="کد های تخفیف"

class OrderDetail(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,verbose_name="سبد سفارش")
    product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name="محصول")
    final_price=models.IntegerField(verbose_name="قیمت نهایی تکی محصول",null=True,blank=True)
    count=models.IntegerField(verbose_name="تعداد")

    def __str__(self):
        return f"{self.order.user.get_full_name()}-{self.product.title}"

    class Meta:
        verbose_name="جزئیات سبد خرید"
        verbose_name_plural="لیست جزئیات سبد های خرید"


class ShippingCost(models.Model):
    province = models.CharField(max_length=50, verbose_name="استان")
    city = models.CharField(max_length=50, verbose_name="شهر", null=True, blank=True)
    price = models.IntegerField(verbose_name="هزینه ارسال")

    def __str__(self):
        return f"{self.province} - {self.city or 'کل استان'}"