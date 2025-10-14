from django import forms

from . import config


class ChatForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": config["PLACEHOLDER"],
                "class": "chat__textarea",
                "rows": 1,
            }
        ),
    )
