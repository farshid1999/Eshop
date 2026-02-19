from django.contrib import admin
from . import models
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_filter = ["title","category","is_active"]
    list_display = ["title","price","is_active","is_delete"]

class ProductCatogory(admin.ModelAdmin):
    pass

class ProductTag(admin.ModelAdmin):
    pass

class CommentProduct(admin.ModelAdmin):
    list_display = ["user"]

admin.site.register(models.Product,ProductAdmin)
admin.site.register(models.ProductCatogory)
admin.site.register(models.ProductTag)
admin.site.register(models.PruductBrand)
admin.site.register(models.VisitedProduct)
admin.site.register(models.SampleProductImages)
admin.site.register(models.CommentsProduct)
