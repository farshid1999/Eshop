from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from .forms import ProfileSettingsModelForm, ResetPasswordForm, AddressForm
from acount_module.models import User
from order_module.models import OrderDetail,Order
from product_model.models import Product
from django.http import JsonResponse, HttpResponse


@method_decorator(login_required,name='dispatch')
class UserPanelView(TemplateView):
    template_name = 'user_module/user_panel.html'


    def get(self, request, *args, **kwargs):
        context = super(UserPanelView, self).get_context_data(*args, **kwargs)

        current_user = User.objects.get(id=request.user.id)

        profile_settings_form=ProfileSettingsModelForm(instance=current_user)
        reset_password_form = ResetPasswordForm

        order=Order.objects.filter(user_id=request.user.id,is_paid=True)
        order_detail=OrderDetail.objects.filter(order__in=order)
        favorite_product=current_user.favorite.all()

        address_form = AddressForm()
        context["address_form"] = address_form
        context["favorite_product"]=favorite_product
        context["order_detail"]=order_detail
        context["profile_settings_form"]=profile_settings_form
        context["reset_password_form"] = reset_password_form

        return render(request,'user_module/user_panel.html',context)

    def post(self,request,*args,**kwargs):
            current_user = User.objects.get(id=request.user.id)
            if "submit_profile" in request.POST or request.FILES:
                profile_form=ProfileSettingsModelForm(request.POST,request.FILES,instance=current_user)
                if profile_form.is_valid():
                    profile_form.save(commit=True)
                    return redirect("user_page")

            if "submit_address" in request.POST:
                form = AddressForm(request.POST)
                if form.is_valid():
                    addr = form.save(commit=False)
                    addr.user = request.user
                    addr.save()
                    return redirect("user_page")

            if "submit_password" in request.POST:
                reset_password_form=ResetPasswordForm(request.POST)
                if reset_password_form.is_valid():
                    user=User.objects.filter(id=request.user.id).first()
                    if user.check_password(reset_password_form.cleaned_data.get("old_password")):
                        user.set_password(reset_password_form.cleaned_data.get("confirm_password"))
                        user.save()
                        logout(request)
                        return redirect("login_page")
                    else:
                        reset_password_form.add_error("confirm_password","کلمه عبور اشتباه است")

            context = super(UserPanelView, self).get_context_data(*args, **kwargs)

            profile_settings_form = ProfileSettingsModelForm(instance=current_user)
            reset_password_form = ResetPasswordForm

            context["profile_settings_form"] = profile_settings_form
            context["reset_password_form"] = reset_password_form

            return render(request,'user_module/user_panel.html')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)



@login_required()
def user_panel_component(request):
   return render(request,'user_module/component/user_panel_component.html')

@login_required()
def add_to_favorite(request):
    product_id = request.GET.get("product_id")
    user_id = request.user.id
    current_product = Product.objects.filter(id=product_id, is_active=True, is_delete=False).first()


    if current_product:
        user = User.objects.get(id=user_id)
        is_exist_favorite=user.favorite.filter(id=product_id).exists()
        if is_exist_favorite:
            user.favorite.remove(current_product)
            user.save()
            return JsonResponse({
                'status': 'warning',
            })
        else:
            user.favorite.add(current_product)
            user.save()
            return JsonResponse({
                'status': 'success',
            })
    else:
        return redirect('home-page')

from django.http import JsonResponse
from .utils import load_iran_states

@login_required
def get_cities(request):
    province = request.GET.get("province")
    data = load_iran_states()

    if province not in data:
        return JsonResponse({"cities": []})

    return JsonResponse({"cities": data[province]})