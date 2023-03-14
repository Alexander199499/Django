import form as form
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.datetime_safe import datetime
from django.views import View
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm
from django.shortcuts import redirect, render
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin




class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'

@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        premium_group.user_set.add(user)
    return redirect('/')

class MyView(PermissionRequiredMixin, View):
    permission_required = ('<app>.<action>_<model>',
                           '<app>.<action>_<model>')

class AddPost(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post', )

class ChangePost(PermissionRequiredMixin, CreateView):
    permission_required = ('news.change_post', )






