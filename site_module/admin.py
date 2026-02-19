from django.contrib import admin
from .models import SiteSetting,FooterLink,FooterLinkBox,Slider,SiteBanner
# Register your models here.


class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ['title','url']

class SliderAdmin(admin.ModelAdmin):
    list_display = ['title','url','is_active']
    list_editable = ['url','is_active']

class BannerAdmin(admin.ModelAdmin):
    list_display = ['title','posation','url']

admin.site.register(SiteSetting)
admin.site.register(FooterLinkBox)
admin.site.register(FooterLink,FooterLinkAdmin)
admin.site.register(Slider,SliderAdmin)
admin.site.register(SiteBanner,BannerAdmin)
