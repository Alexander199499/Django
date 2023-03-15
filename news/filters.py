from .models import *
from django_filters import FilterSet, CharFilter, DateTimeFilter, ModelChoiceFilter
from django import forms


class Meta:
    model = Post
    fields = {
           'author',
           'title',
           'time_created',
               }

class ProductFilter(FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains', label='Поиск по заголовку')
    author = ModelChoiceFilter(field_name = 'author', queryset = Author.objects.all(), label = 'Имя автора')
    time_created = DateTimeFilter(field_name='time_created', widget=forms.DateInput(attrs={'type': 'date'}), lookup_expr='date__gt', label='Поиск по дате')


