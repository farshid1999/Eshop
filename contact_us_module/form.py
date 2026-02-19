from django import forms
from .models import ContactUs

class ProfileForm(forms.ModelForm):
    image_field=forms.FileField()



class ContactUsModelForm(forms.ModelForm):
    class Meta:
        model=ContactUs
        fields=["title","fulname","email","message"]
        # labels = {
        #     'title': 'Title of the message',
        #     'fulname': 'Full Name',
        #     'email': 'Email Address',
        #     'message': 'Message',
        #     'is_reade_by_admin': 'Is read by admin?',
        #     'response': 'Admin response',
        #     'create_date': 'Date of creation',
        # }
        # help_texts = {
        #     'email': 'Please enter a valid email address.',
        #     'message': 'Describe your inquiry in detail.',
        #     'create_date': 'Enter the date when the message was created.',
        # }
        error_messages = {
            'title': {
                'required': 'موضوع خود را وارد کنید',
                'max_length': 'نمیتوانید بیشتر از 50 کارکتر استفاده کنید',
            },
            'email': {
                'invalid': 'ایمیل خود را به درستی وارد کنید',
            },
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان'}),
            'fulname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام و نام خانوادگی'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل'}),
            'message': forms.Textarea(attrs={'class': 'form-control','id':'message','rows':'8', 'placeholder': 'متن'}),
        }





class ContactUsForm(forms.Form):
    fullname=forms.CharField(max_length=50
                             ,required=True
                             ,template_name="fullname"
                             ,error_messages={
            "required":"نام و نام خانوادگی خود را وارد کنید",
            "max_length":" نمی توانید بیشتر از 50 کارکتر وارد کنید",
        }
                             ,widget=forms.TextInput(attrs={
            "class":"form-control",
            "placeholder":"نام و نام خانوادگی"
        }))
    email=forms.EmailField(max_length=50
                           ,required=True
                           ,template_name="email"
                           ,error_messages={
            "required": "ایمیل خود را وارد کنید",
            "max_length": " نمی توانید بیشتر از 50 کارکتر وارد کنید",
        }
                           ,widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "ایمیل"
        })
                           )
    subject=forms.CharField(max_length=50
                            ,required=True
                            ,template_name="subject"
                            ,error_messages={
            "required": "موضوع خود را وارد کنید",
            "max_length": " نمی توانید بیشتر از 50 کارکتر وارد کنید",
        }
                            ,widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "موضوع"
        }))
    text=forms.CharField(required=True
                         ,template_name="text"
                         ,error_messages={
            "required": "متن خود را وارد کنید",
        }
                         ,widget=forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": "متن پیام",
            "id":"message",
            "rows":"8"
        }))

