from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View

from .filters import ProductFilter
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import PostForm
from .models import *
from django import forms



class PostList(ListView):
    model = Post
    ordering = '-time_created'
    template_name = 'news.html'
    context_object_name = 'post'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ProductFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'news_pk.html'
    context_object_name = 'post'

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        form.save()
        return HttpResponseRedirect('/news')
    form = PostForm()
    return render(request, 'post_create.html', {'form': form})

class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    success_url = reverse_lazy('post_list')
    permission_required = ('<app>.<action>_<model>',
                           '<app>.<action>_<model>')
    permission_required = ('news.change_post')

    def form_valid(self, form):
        news = form.save(commit=False)
        news.post_type = 'NE'
        return super().form_valid(form)

class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    permission_required = ('<app>.<action>_<model>',
                           '<app>.<action>_<model>')
    permission_required = ('news.change_post')


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = ('<app>.<action>_<model>',
                           '<app>.<action>_<model>')
    permission_required = ('news.change_post')

class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'
    permission_required = ('<app>.<action>_<model>',
                           '<app>.<action>_<model>')
    permission_required = ('news.change_post')

    def form_valid(self, form):
        article = form.save(commit=False)
        article.post_type = 'AR'
        return super().form_valid(form)

class ArticleUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'
    permission_required = ('<app>.<action>_<model>',
                           '<app>.<action>_<model>')
    permission_required = ('news.change_post')


class MyView(PermissionRequiredMixin, View):
    permission_required = ('<app>.<action>_<model>',
                           '<app>.<action>_<model>')

class AddPost(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')

class ChangePost(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')

class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.categories = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(categories=self.categories).order_by('-time_created')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscribe'] = self.request.user not in self.categories.subscribers.all()
        context['categories'] = self.categories
        return context

@login_required
def subscribe(request, pk):
   user = request.user
   categories = Category.objects.get(id=pk)
   categories.subscribes.add(user)

   message = 'Вы успешно подписались на рассылку новостей'
   return render(request, 'subscribe.html', {'categories': categories, 'message': message})






