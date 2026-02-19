from django.db.models import Count, Sum
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.base import TemplateView
# Create your views here.
from site_module.models import SiteSetting, FooterLinkBox,Slider
from product_model.models import Product,ProductCatogory
import numpy as np

class HomeView(TemplateView):
    template_name='home_module/home_page.html'

    def get_context_data(self, **kwargs):
        context=super(HomeView, self).get_context_data(**kwargs)
        slider:Slider=Slider.objects.filter(is_active=True)
        product:Product=Product.objects.filter(is_active=True,is_delete=False).order_by("-id")[:8]
        categories = list(ProductCatogory.objects.filter(is_active=True, is_delete=False))
        most_visit_product=Product.objects.filter(is_active=True,is_delete=False).annotate(visit_count=Count("visitedproduct")).order_by("-visit_count")[:8]
        parent_categories = ProductCatogory.objects.filter(parent__isnull=True, is_active=True, is_delete=False)
        most_bought_product=Product.objects.filter(orderdetail__order__is_paid=True).annotate(order_count=Sum(
            'orderdetail__count'
        )).order_by('-order_count')[:8]


        products = Product.objects.filter(is_active=True, is_delete=False)
        favorite_ids = set(
            self.request.user.favorite.values_list('id', flat=True)) if self.request.user.is_authenticated else set()
        favorite_map = {product.id: (product.id in favorite_ids) for product in products}

        products_categories = []
        for category in categories:
            subcategories = ProductCatogory.objects.filter(parent=category, is_active=True, is_delete=False)
            item = {
                "id": category.id,
                "title": category.title,
                "sub_category": [
                    {
                     "id": sub.id,
                     "title": sub.title,
                     "sub_product":list(Product.objects.filter(is_delete=False,is_active=True,category=sub).all()[:4])}for sub in subcategories
                ]
            }
            products_categories.append(item)

        context["parent_category"]=parent_categories
        context["products_categories"] = products_categories
        context['slider']=slider
        context["favorite_map"]=favorite_map
        context["latest_product"]=np.reshape(product,(2,4))
        context["most_visit_product"]=np.reshape(most_visit_product,(2,4))
        context["most_bought_product"]=group_list(most_bought_product)
        return context


def site_header_component(request):
    setting : SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    context = {
        'site_setting': setting
    }
    return render(request,'shared/site_header_component.html',context)
def site_footer_component(request):
    setting : SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    footer_link_boxes=FooterLinkBox.objects.all()
    for item in footer_link_boxes:
        item.footerlink_set
    context = {
        'site_setting': setting,
        'footer_link_boxes':footer_link_boxes
    }
    return render(request,'shared/site_footer_component.html',context)


class AboutUsView(TemplateView):
    template_name = 'home_module/about_us.html'

    def get_context_data(self,*args,**kwargs):
        context =super(AboutUsView,self).get_context_data(*args,**kwargs)
        site_setting :SiteSetting=SiteSetting.objects.filter(is_main_setting=True).first()
        context['site_setting']=site_setting
        return context



def group_list(arr, size=4):
    grouped_list=[]
    for i in range(0,len(arr),size):
        grouped_list.append(arr[i:i+size])
    return grouped_list
