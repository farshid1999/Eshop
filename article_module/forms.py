from django import forms
from .models import ArticleComments

class ArticleCommentsModelForm(forms.ModelForm):
    class Meta:
        model = ArticleComments
        fields=["text"]
        widgets={
            "text":forms.Textarea(attrs={
                "placeholder":"نظر خود را وارد کنید",
                "rows":"11",
                "style":"background-color: white;outline-color: orange",
                "id":"comment_text"
            })
        }
