from django import forms


class ChatForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Type your message here...",
                "class": "chat__textarea",
                "rows": 1,
            }
        ),
    )
