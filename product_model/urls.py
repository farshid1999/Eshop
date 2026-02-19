from django.urls import path
from . import views
urlpatterns=[
    path('',views.ProductListView.as_view(),name='list_page'),
    path('cat/<category_product>',views.ProductListView.as_view(),name='filter_category_product'),
    path('brand/<brand_product>',views.ProductListView.as_view(),name='filter_brand_product'),
    path('<str:slug>', views.ProductDetailView.as_view(),name='detail_list')
]
