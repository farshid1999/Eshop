from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.generic import ListView

from site_module.models import SiteSetting
from .form import ContactUsForm,ContactUsModelForm,ProfileForm
from .models import ContactUs,Profile
from django.views.generic.base import TemplateView,View
from django.views.generic.edit import FormView,CreateView
# Create your views here.

class ContactUsView(CreateView):
    template_name = "contact_us_module/contact_us.html"
    form_class = ContactUsModelForm
    success_url = "/contact-us/"

    def get_context_data(self,*args, **kwargs):
        context=super().get_context_data(*args,**kwargs)
        setting : SiteSetting=SiteSetting.objects.filter(is_main_setting=True).first()
        context["site_setting"]=setting
        return context

    # def form_valid(self, form):
    #     form.save()
    #     return super().form_valid(form)

def store_file(file):
    with open("temp/image.jpg",'wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)

class CreatProfileView(CreateView):
    model = Profile
    template_name = "contact_us_module/profile_page.html"
    fields = "__all__"
    success_url = "profile-page"

class ProfilesView(ListView):
    model = Profile
    template_name = "contact_us_module/profile_list.html"
    context_object_name = "profiles"

    # def get(self,request):
    #     form=ProfileForm()
    #     return render(request,"contact_us_module/profile_page.html",{"form":form})
    # def post(self,request):
    #     submitted_form=ProfileForm(request.POST,request.FILES)
    #     if submitted_form.is_valid():
    #         profile=Profile(image=request.FILES["image_field"])
    #         profile.save()
    #         return redirect('profile-page')
    #     return render(request,'contact_us_module/profile_page.html',{"form":submitted_form})





    # def get(self, request, *args, **kwargs):
    #     contact_us=ContactUsForm()
    #     return render(request,'contact_us_module/contact_us.html',{"contact_form":contact_us})
    #
    # def post(self,request):
    #     success=False
    #     cleaned_data=None
    #     contact_us=ContactUsForm(request.POST)
    #     if contact_us.is_valid():
    #         cleaned_data=contact_us.cleaned_data
    #         ContactUs.objects.create(
    #             title=cleaned_data["subject"],
    #             email = cleaned_data['email'],
    #             fullname = cleaned_data['fullname'],
    #             message = cleaned_data['text'],
    #             response = '',
    #             is_reade_by_admin = False
    #         )
    #         success=True
    #         return redirect(request,'home-page')
    #
    #     return render(request,'contact_us_module/contact_us.html',{"contact_form":contact_us,
    #                                                            "succsess":success,
    #                                                            "cleaned_data":cleaned_data})




# def contact_us_page(request):
#     success=False
#     cleaned_data=None
#     if request.method=="POST":
#         contact_us=ContactUsForm(request.POST)
#         if contact_us.is_valid():
#             cleaned_data=contact_us.cleaned_data
#             ContactUs.objects.create(
#                 title=cleaned_data['subject'],
#                 email=cleaned_data['email'],
#                 fulname=cleaned_data['fullname'],
#                 message=cleaned_data['text'],
#                 response='',
#                 is_reade_by_admin=False
#             )
#             success=True
#
#     contact_us=ContactUsForm()
#     return render(request,'contact_us_module/contact_us.html',{"contact_form":contact_us,
#                                                                "succsess":success,
#                                                                "cleaned_data":cleaned_data})
