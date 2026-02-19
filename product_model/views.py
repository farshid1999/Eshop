from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from jalali_date import date2jalali

from .models import Product,ProductCatogory,PruductBrand,VisitedProduct,SampleProductImages,CommentsProduct
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.db.models import Avg,Count
from django.views.generic.base import TemplateView
from django.views.generic import ListView,DetailView
from tools.get_ip import get_ip
import numpy as np
# Create your views here.

class ProductListView(ListView):
    template_name = "product_model/product_list.html"
    model=Product
    context_object_name = "product"
    paginate_by = 6


    def get_queryset(self):
        query=super(ProductListView,self).get_queryset()
        category_selected=self.kwargs.get("category_product")
        if category_selected is not None:
            query=query.filter(category__url_title__iexact=category_selected)

        brand_selected=self.kwargs.get("brand_product")
        if brand_selected is not None:
            query=query.filter(brand__url_title__iexact=brand_selected)

        request=self.request
        start_price=request.GET.get("start_price")
        end_price=request.GET.get("end_price")

        if start_price is not None:
            query =query.filter(price__gte=start_price)

        if end_price is not None:
            query=query.filter(price__lte=end_price)

        return query

    def get_context_data(self,*args, **kwargs):
        context=super(ProductListView,self).get_context_data(*args,**kwargs)

        products = Product.objects.filter(is_active=True, is_delete=False)
        favorite_ids = set(
            self.request.user.favorite.values_list('id', flat=True)) if self.request.user.is_authenticated else set()
        favorite_map = {product.id: (product.id in favorite_ids) for product in products}

        max_product_price :Product=Product.objects.all().order_by("-price").first().price or 0

        context["favorite_map"]=favorite_map
        context["start_price"]=self.request.GET.get("start_price") or 0
        context["end_price"]=self.request.GET.get("end_price") or max_product_price
        return context


def brand_product_component(request):
    product_brand = PruductBrand.objects.filter(is_active=True)
    context = {
        "product_brand": product_brand
    }
    return render(request, "product_model/component/brand_product_component.html", context)

def category_product_component(request):
    product_categories=ProductCatogory.objects.filter(is_active=True,is_delete=False)
    context={
        "product_categories":product_categories
    }
    return render(request,"product_model/component/category_product_component.html",context)

# def brand_product_component(request):
#     product_brand=PruductBrand.objects.filter(is_active=True)
#     context={
#         "product_brand":product_brand
#     }
#     return render(request,"product_model/component/brand_product_component.html",context)

class ProductDetailView(DetailView):
    template_name = "product_model/product_detail.html"
    model = Product

    def get_context_data(self,*args,**kwargs):
        context=super(ProductDetailView,self).get_context_data(*args,**kwargs)
        loaded_product=self.object
        user_ip=get_ip(self.request)
        user_id=None
        if self.request.user.is_authenticated:
            user_id=self.request.user.id
        if not VisitedProduct.objects.filter(ip__iexact=user_ip,product_id=loaded_product.id).exists():
            new_visit=VisitedProduct(ip=user_ip,product_id=loaded_product.id,user_id=user_id)
            new_visit.save()

        current_sample_images=list(SampleProductImages.objects.filter(product_id=loaded_product.id).all()[:6])
        suggestion_product=group_list(list(Product.objects.filter(brand_id=loaded_product.brand.id).exclude(pk=loaded_product.id).all()[:6]),3)
        comments=CommentsProduct.objects.filter(product_id=loaded_product.id).all()
        count_comment=CommentsProduct.objects.filter(product_id=loaded_product.id).count()

        context["count_comments"]=count_comment
        context["comments"]=comments
        context["sample_images"]=group_list(current_sample_images,3)
        context["suggest_product"]=suggestion_product

        return context

    def post(self, request, *args, **kwargs):
        slug=self.kwargs.get("slug")
        if request.method == "POST":
            comment_text = request.POST.get("comment-text-name")
            product_id = request.POST.get("product-id-name")
            user_id = request.POST.get("user-id-name")
            if comment_text !="":
                comment = CommentsProduct(user_id=user_id, product_id=product_id, comment=comment_text)
                comment.save()
                return redirect("detail_list", slug=slug)
            else:
                return redirect("detail_list", slug=slug)


        return redirect("detail_list",slug=slug)

def group_list(arr, size):
    grouped_list=[]
    for i in range(0,len(arr),size):
        grouped_list.append(arr[i:i+size])
    return grouped_list

        # slug=self.kwargs.get("slug")
        # product_count=Product.objects.filter(slug=slug).get_or_create("count")
        # context["count"]=product_count



# def product_list(request):
#     # select_product="select * from product_model_product order by title"
#     # count_product=Product.objects.aggregate(Count("id"))
#     # products=Product.objects.raw(select_product)
#     products=Product.objects.all().order_by('-price')[:5]
#     return render(request,'product_model/product_list.html',{"product":products})


# class ProductDetailView(TemplateView):
#     template_name = "product_model/product_detail.html"
#     def get_context_data(self, **kwargs):
#         context=super(ProductDetailView,self).get_context_data()
#         product_slug=kwargs["slug"]
#         product=get_object_or_404(Product,slug=product_slug)
#         count_product = Product.objects.filter(slug=product_slug).aggregate(Count("id"))
#         context["product"]=product
#         context["count_product"]=count_product["id__count"]
#         return context

# def product_detail(request,slug):
#     SQL=f"select * from product_model_product where slug ='{slug}'"
#     product=Product.objects.raw(SQL)
#     product = product[0] if product else None
#     if product is None:raise Http404()
#
#     count_product=Product.objects.filter(slug=slug).aggregate(Count("id"))
#     product = get_object_or_404(Product, slug=slug)
#     # product=get_object_or_404(Product,pk=product_id)
#     return render(request,'product_model/product_detail.html',{"product":product,"product_count":count_product["id__count"]})
#
