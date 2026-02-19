from django import forms
from acount_module.models import User
from django.core.exceptions import ValidationError
from django.core import validators
class ProfileSettingsModelForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["first_name","last_name","username","about_user","address","avatar"]
        widgets={
            "first_name":forms.TextInput(attrs={'style':'margin-bottom:10px', 'class': 'form-control', 'placeholder': 'نام'}),
            "last_name": forms.TextInput(attrs={'style':'margin-bottom:10px','class': 'form-control', 'placeholder': 'نام خانوادگی'}),
            "username": forms.TextInput(attrs={'style':'margin-bottom:10px','class': 'form-control', 'placeholder': 'نام کاربری'}),
            "about_user": forms.Textarea(attrs={'style':'margin-bottom:10px','class': 'form-control', 'placeholder': 'درباره من'}),
            "address": forms.Textarea(attrs={'style':'margin-bottom:10px','class': 'form-control', 'placeholder': 'آدرس'}),
            "avatar": forms.FileInput(attrs={'style':'margin-bottom:10px;display:none','id':'edit-avatar','class': 'form-control'}),
        }
        labels={
            "first_name":"",
            "last_name": "",
            "username": "",
            "about_user": "",
            "address": "",
            "avatar": "",
        }
        help_texts={
            "first_name": "",
            "last_name": "",
            "username": "",
            "about_user": "",
            "address": "",
            "avatar": "",
        }


class ResetPasswordForm(forms.Form):
    old_password=forms.CharField(
        help_text="",
        label="",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "رمز عبور فعلی",
                'class': 'form-control',
                'style': 'margin-bottom:10px'
            }
        )
    )

    password=forms.CharField(
        help_text="",
        label="",
        widget=forms.PasswordInput(attrs={
            "placeholder":"رمز عبور",
            'class': 'form-control',
            'style': 'margin-bottom:10px'
        })
    )
    confirm_password=forms.CharField(
        help_text="",
        label="",
        widget=forms.PasswordInput(attrs={
            "placeholder":" تکرار رمز عبور",
            'class': 'form-control',
            'style': 'margin-bottom:10px'
        })
    )

    def clean_confirm_password(self):
        password=self.cleaned_data.get("password")
        confirm_password=self.cleaned_data.get("confirm_password")
        if password == confirm_password:
            return confirm_password
        else:
            return ValidationError("تکرار کلکه عبور اشتباه است")


# user_module/forms.py
from django import forms
from acount_module.models import Address
from .utils import load_iran_states

class AddressForm(forms.ModelForm):
    province = forms.ChoiceField(label="استان")
    city = forms.ChoiceField(label="شهر")

    class Meta:
        model = Address
        fields = ["province", "city", "postal_code", "detail"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        data = load_iran_states()

        self.fields["province"].choices = [(p, p) for p in data.keys()]
        self.fields["city"].choices = []
