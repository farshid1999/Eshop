import time

from django.http import HttpRequest, HttpResponse,JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.urls import reverse

from order_module.models import Order, OrderDetail, Discount, ShippingCost
from product_model.models import Product
import requests
import json

def add_product_to_order(request:HttpRequest):
    product_id=int(request.GET.get("product_id"))
    count=int(request.GET.get("count"))
    if count<=0:
        return JsonResponse({
            "status":"invalid_count",
            "title":"هشدار!",
            "text":"مقدار وارد شده صحیح نمی باشد",
            "icon":"error"
        })

    if request.user.is_authenticated:
        product=Product.objects.filter(id=product_id,is_active=True,is_delete=False).first()
        if product is not None:
            order,flag=Order.objects.get_or_create(user_id=request.user.id,is_paid=False)
            order_detail=order.orderdetail_set.filter(product_id=product_id,order__is_paid=False).first()
            if order_detail is not None:
                order_detail.count=count
                order_detail.save()
                return JsonResponse({
                    "status": "save_product",
                    "title": "موفق",
                    "text": "سفارش شما به سبد خرید افزوده شد",
                    "icon": "success"

                })

            else:
                order_detail=OrderDetail(product_id=product_id,count=count,order_id=order.id)
                order_detail.save()
                return JsonResponse({
                    "status": "save_product",
                    "title": "موفق",
                    "text": "سفارش شما به سبد خرید افزوده شد",
                    "icon": "success"
                })
        else:
            return JsonResponse({
                "status": "not_product",
                "title": "موفق",
                "text": "محصولی با مشخصات وارد شده یافت نشد",
                "icon": "error"

            })

    else:
        return JsonResponse({
            "status":"not_auth",
            "title": "هشدار!",
            "text": "برای سفارش ابتدا وارد حساب کاربری شوید",
            "icon": "info"
        })
@login_required()
def delete_product_order(request):
    product_id=request.GET.get("product_id")
    try:
        product_id = int(product_id)
        if product_id < 0:
            raise ValueError("شناسه محصول منفی است")
    except (ValueError, TypeError):
        return JsonResponse({
            "status": "product_id_invalid"
        })
    order = Order.objects.get(user_id=request.user.id, is_paid=False)
    delete_order=OrderDetail.objects.filter(order__user_id=request.user.id,product_id=product_id,order_id=order.id,order__is_paid=False).first()
    if delete_order is not None:
        delete_order.delete()
        return JsonResponse({
            "status": "delete_succese"
        })
    else:
        return JsonResponse({
            "status":"product_not_found"
        })

@login_required()
def order_products(request):
    user_id=request.user.id
    current_order=OrderDetail.objects.filter(order__user_id=user_id,order__is_paid=False).all()
    final_price = sum(co.product.price * co.count for co in current_order)
    context={
        "orders":current_order,
        "final_price":final_price
    }

    return render(request,'order_module/order_page.html',context)

@login_required()
def increse_product_count(request):
    product_id = int(request.GET.get("product_id"))
    count = int(request.GET.get("count"))
    try:
        product_id = int(product_id)
        count = int(count)
    except:
        return redirect("order_page")

    if product_id and count and count > 0:
        current_order = OrderDetail.objects.filter(order__user_id=request.user.id, product_id=product_id,order__is_paid=False).first()
        current_order.count = count
        current_order.save()
        return JsonResponse({
            'status':'succses',
            'new_count':current_order.count
        })
    else:
        return JsonResponse({
            'status':'faild'
        })


@login_required()
def decrease_product_count(request):
    try:
        product_id=int(request.GET.get("product_id"))
        count = int(request.GET.get("count"))
    except:
        return redirect("order_page")

    current_order=OrderDetail.objects.filter(order__user_id=request.user.id,product_id=product_id,order__is_paid__exact=False).first()
    current_order.count=count
    current_order.save()

@login_required()
def is_valid_discount(request):
    discount_code=request.GET.get('code')
    user_id=request.GET.get('userid')
    current_discount=Discount.objects.filter(user_id=user_id,is_active=True,is_used=False,discount_code__iexact=discount_code,discount_price=200000).first()
    current_order = OrderDetail.objects.filter(order__user_id=user_id).all()
    price = sum(co.product.price * co.count for co in current_order)
    if current_discount:
        final_price = price - current_discount.discount_price
        return JsonResponse({
            'status':'succese',
            "title": "موفق",
            "text": "کد تخفیف اعمال شد",
            "icon": "success",
            'final_price':final_price
        })
    else:
        return JsonResponse({
            'status':'error',
            "title": "هشدار!",
            "text": "کد وارد شده معتبر نمیباشد",
            "icon": "error"
        })


MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
amount = 11000  # Rial / Required
description = "نهایی کردن خرید شما از سایت ما"  # Required
email = ''  # Optional
mobile = ''  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8000/order/verify-payment/'


@login_required
def request_payment(request: HttpRequest):
    current_order,created=Order.objects.get_or_create(is_paid=False,user_id=request.user.id)
    total_price=current_order.calculate_total_price()
    if total_price==0:
        return redirect(reverse('order_page'))
    req_data = {
        "merchant_id": MERCHANT,
        "amount": total_price * 10,
        "callback_url": CallbackURL,
        "description": description,
        # "metadata": {"mobile": mobile, "email": email}
    }
    req_header = {"accept": "application/json", "content-type": "application/json'"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(req_data), headers=req_header)
    authority = req.json()['data']['authority']
    if len(req.json()['errors']) == 0:
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")

@login_required
def verify_payment(request: HttpRequest):
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_price = current_order.calculate_total_price()
    t_authority = request.GET['Authority']
    if request.GET.get('Status') == 'OK':
        req_header = {"accept": "application/json", "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": total_price * 10,
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                current_order.is_paid=True
                current_order.payment_date=time.time()
                current_order.save()
                return HttpResponse('Transaction success.\nRefID: ' + str(
                    req.json()['data']['ref_id']
                ))
            elif t_status == 101:
                return HttpResponse('Transaction submitted : ' + str(
                    req.json()['data']['message']
                ))
            else:
                return HttpResponse('Transaction failed.\nStatus: ' + str(
                    req.json()['data']['message']
                ))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
    else:
        return HttpResponse('Transaction failed or canceled by user')


@login_required
def calculate_shipping(request):
    province = request.GET.get("province")
    city = request.GET.get("city")  # اگر نیاز نداشتی حذف کن

    if not province:
        return JsonResponse({"status": "error", "msg": "استان ارسال نشده"})


    shipping = ShippingCost.objects.filter(province=province).first()

    if shipping is None:
        return JsonResponse({"status": "not_found"})

    return JsonResponse({
        "status": "ok",
        "price": shipping.price
    })

from user_module.utils import load_iran_states

def order_view(request):
    data = load_iran_states()
    provinces = list(data.keys())
    return render(request, "order.html", {"provinces": provinces})