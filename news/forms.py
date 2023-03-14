from django import forms
from django.core.exceptions import ValidationError
from .models import *


class PostForm(forms.ModelForm):

    text = forms.Textarea()
    author = forms.ModelChoiceField(label='Имя автора', queryset = Author.objects.all())
    title = forms.CharField(label='Заголовок')
    category = forms.ModelChoiceField(label='Выберите категорию', queryset=Category.objects.all())


    class Meta:

        model = Post
        fields = [
            'author',
            'title',
            'text',
            'category',

        ]
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")
        if title == text:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )
        return cleaned_data