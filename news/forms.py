from django import forms
from django.core.exceptions import ValidationError

from .models import Post

class PostForm(forms.ModelForm):
    # title = forms.CharField(max_length=200)

    class Meta:
        model = Post
        fields = [
            'title',
            'author',
            'post_category',
            'content',
        ]

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("title")
        content = cleaned_data.get("content")

        if name == content:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data