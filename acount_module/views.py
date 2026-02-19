from django.http import HttpResponse
from django.shortcuts import render, redirect,reverse,get_object_or_404,Http404
from django.contrib.auth import get_user_model
from django.views import View
from .forms import RegisterForm,LoginForm,ForgotPassForm,ResetPassForm
from .models import User
from django.utils.crypto import get_random_string
from django.contrib.auth import login,logout,authenticate
from .utils.email_service import send_email
# Create your views here.


class RegisterView(View):
    def get(self,request):
        register_form=RegisterForm()
        context={
            "register_form":register_form
        }
        return render(request,'acount_module/register_page.html',context=context)

    def post(self,request):
        register_form=RegisterForm(request.POST)
        if register_form.is_valid():
            user_email=register_form.cleaned_data.get('email')
            user_password=register_form.cleaned_data.get('password')
            user_name=register_form.cleaned_data.get('user_name')

            user:bool=User.objects.filter(email__exact=user_email).exists()
            user_name_bool:bool=User.objects.filter(username=user_name).exists()
            if user or user_name_bool:
                register_form.add_error(user_email,'ایمیل یا نام کاربری تکراری میباشد')
            else:
                new_user=User(email=user_email,email_active_code=get_random_string(72),username=user_name,is_active=False)
                new_user.set_password(user_password)
                new_user.save()
                send_email('فعال سازی حساب کاربری',new_user.email,{'user':new_user},'email/active_account.html')

                return redirect(reverse('login_page'))
        context = {
            "register_form": register_form
        }
        return render(request, 'acount_module/register_page.html', context=context)

class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        context = {
            "login_form": login_form
        }
        return render(request, 'acount_module/login_page.html', context=context)

    def post(self, request):
        login_form=LoginForm(request.POST)
        if login_form.is_valid():
            user_name_form=login_form.cleaned_data.get('user')
            password_form=login_form.cleaned_data.get('password')
            user : User=User.objects.filter(username=user_name_form).first()
            if user is not None:
                if not user.is_active:
                    login_form.add_error('user','حساب کاربری شما غیر فعال است')
                else:
                    is_pass_correct = user.check_password(password_form)
                    if is_pass_correct:
                        login(request,user)
                        request.session['username'] = user.username
                        return redirect(reverse('home-page'))
                    else:
                        login_form.add_error('user', 'کاربری با این مشخصات یافت نشد')
            else:
                login_form.add_error('user','کاربری با این مشخصات یافت نشد')
        context = {
            "login_form": login_form,
        }
        return render(request, 'acount_module/login_page.html', context=context)


class ActiveAccountView(View):
    def get(self,request,active_code):
        user : User = User.objects.filter(email_active_code__exact=active_code).first()
        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.email_active_code = get_random_string(72)
                user.save()
                return redirect(reverse('login_page'))
            else:
                raise Http404

        else:
            raise Http404


class ForgotPassView(View):
    def get(self,request):
        forgot_pass_form=ForgotPassForm()
        context={
            "forgot_pass":forgot_pass_form
        }
        return render(request,'acount_module/forgot_pass_page.html',context=context)

    def post(self,request):
        forgot_pass_form=ForgotPassForm(request.POST)
        if forgot_pass_form.is_valid():
            user_email = forgot_pass_form.cleaned_data.get('email')
            user: User = User.objects.filter(email__exact=user_email).first()
            if user is not None:
                #todo:send email
                send_email('فعال سازی حساب کاربری', user.email, {'user': user}, 'email/active_account.html')
            else:
                forgot_pass_form.add_error('email', 'ایمیل یافت نشد')

        context = {
            "forgot_pass": forgot_pass_form
        }
        return render(request, 'acount_module/forgot_pass_page.html', context=context)


class ResetPass(View):
    def get(self,request,active_code):
        user:User=User.objects.filter(email_active_code__exact=active_code).first()
        if user is not None:
            reset_pass_form=ResetPassForm()
            context = {
                "reset_pass_form":reset_pass_form,
                "user":user
            }
            return render(request, 'acount_module/reset_pass_page.html', context=context)

        else:
            return redirect(reverse('login_page'))

    def post(self,request,active_code):
        reset_pass_form = ResetPassForm(request.POST)
        user: User = User.objects.filter(email_active_code__exact=active_code).first()
        if reset_pass_form.is_valid():

            if user is None:
                return redirect(reverse('login_page'))
            user_new_pass=reset_pass_form.cleaned_data.get('confirm_password')
            user.set_password(user_new_pass)
            user.email_active_code=get_random_string(72)
            user.is_active=True
            user.save()
            return redirect(reverse('login_page'))

        context = {
            "reset_pass_form": reset_pass_form,
            "user": user
        }
        return render(request, 'acount_module/reset_pass_page.html', context=context)



class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect(reverse('home-page'))




