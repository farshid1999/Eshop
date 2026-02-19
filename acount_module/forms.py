from django import forms
from django.core.exceptions import ValidationError
from django.core import validators

class RegisterForm(forms.Form):
    user_name=forms.CharField(
        validators=[
            validators.MaxLengthValidator(20)
        ],
        widget=forms.TextInput(
            attrs={
                "placeholder":"نام کاربری"
            }
        )
    )
    email=forms.EmailField(
        validators=[
            validators.MaxLengthValidator(20),
            validators.EmailValidator
        ],
        widget=forms.EmailInput(
            attrs={
                "placeholder":"ایمیل"
            }
        )
    )
    password=forms.CharField(
        validators=[
            validators.MaxLengthValidator(20)
                    ],
        widget=forms.PasswordInput(
            attrs={
                "placeholder":"کلمه عبور"
            }
        )

    )
    confirm_password=forms.CharField(
        validators=[
            validators.MaxLengthValidator(20)
        ],
        widget=forms.PasswordInput(
            attrs={
                "placeholder":"تکرار کلمه عبور"
            }
        )
    )

    def clean_confirm_password(self):
        password=self.cleaned_data.get('password')
        con_pass=self.cleaned_data.get('confirm_password')
        if password == con_pass:
            return con_pass
        else:
            return ValidationError('کلمه عبور اشتباه است')


class LoginForm(forms.Form):
    user=forms.CharField(
        validators=[
          validators.MaxLengthValidator(20)
        ],
        widget=forms.TextInput(
            attrs={
                "placeholder":"نام کاربری"
            }
        )
    )
    password=forms.CharField(
        validators=[
            validators.MaxLengthValidator(20)
        ],
        widget=forms.PasswordInput(
            attrs={
                "placeholder":"رمز عبور"
            }
        )
    )


class ForgotPassForm(forms.Form):
    email = forms.EmailField(
        validators=[
            validators.MaxLengthValidator(50),
            validators.EmailValidator
        ],
        widget=forms.EmailInput(
            attrs={
                "placeholder": "ایمیل"
            }
        )
    )


class ResetPassForm(forms.Form):
    password=forms.CharField(
        validators=[
            validators.MaxLengthValidator(20)
                    ],
        widget=forms.PasswordInput(
            attrs={
                "placeholder":"کلمه عبور"
            }
        )

    )
    confirm_password=forms.CharField(
        validators=[
            validators.MaxLengthValidator(20)
        ],
        widget=forms.PasswordInput(
            attrs={
                "placeholder":"تکرار کلمه عبور"
            }
        )
    )

    def clean_confirm_password(self):
        password=self.cleaned_data.get('password')
        con_pass=self.cleaned_data.get('confirm_password')
        if password == con_pass:
            return con_pass
        else:
            return ValidationError('کلمه عبور اشتباه است')
