from django.urls import path
from . import views
urlpatterns=[
    path('add-to-order',views.add_product_to_order,name="add_product_to_order"),
    path('delete-product-order',views.delete_product_order,name="delete_product_order"),
    path('inc-count-prod',views.increse_product_count,name="increase_product_count"),
    path('dec-count-prod',views.decrease_product_count,name="decrease_product_count"),
    path('product-order',views.order_products,name="order_page"),
    path('discount-order',views.is_valid_discount,name='discount_user'),
    path('request/',views.request_payment,name='request'),
    path('verify/',views.verify_payment,name='verify'),
path("calculate-shipping/", views.calculate_shipping, name="calculate_shipping"),
]
