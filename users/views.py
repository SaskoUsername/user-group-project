from django.contrib.auth import login, logout
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm, LoginForm, GroupCreatingForm, UserCreatingForm
from .models import Group, User


# Create your views here.
@login_required(login_url="login/")
def groups_list(request):
    context = {"groups": Group.objects.all()}
    return render(request, 'groups_list.html', context)


def sign_up_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    elif request.method == 'POST' and not request.user.is_superuser:
        raise ValidationError(_('PermissionDenied'))
    else:
        form = SignUpForm()

    return render(request, "sign_up_page.html", {"form": form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST, request=request)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    elif request.method == 'POST' and not request.user.is_superuser:
        raise ValidationError(_('PermissionDenied'))
    else:
        form = LoginForm()
    return render(request, 'log_in_page.html', {'form': form})


def logout_view(request):
    if (request.user.is_authenticated):
        logout(request)
        return redirect('/')


def get_users_of_group(request, index):
    context = {
        'users': User.objects.filter(group_id_id=index).all(),
        'current_group': Group.objects.filter(id=index).first(),
    }

    return render(request, 'users_list.html', context)


def delete_object_view(request, object_id):
    if request.META.get('HTTP_REFERER') == request.build_absolute_uri(reverse('list_of_groups')):
        Group.objects.filter(id=object_id).delete()
        return redirect('list_of_groups')

    else:
        User.objects.filter(id=object_id).delete()
        return redirect('list_of_groups')


def create_group_view(request):
    if request.method == 'POST':
        form = GroupCreatingForm(request.POST)
        if form.is_valid():
            form.save_group()
            return redirect('list_of_groups')
    elif request.method == 'POST' and not request.user.is_superuser:
        raise ValidationError(_('PermissionDenied'))
    else:
        form = GroupCreatingForm()
    return render(request, "group_update_page.html", {'form': form})


def create_user_view(request, group_id):
    if request.method == 'POST':
        form = UserCreatingForm(request.POST, request)
        if form.is_valid():
            form.save_user(group_id)
            return redirect('list_of_groups')
    elif request.method == 'POST' and not request.user.is_superuser:
        raise ValidationError(_('PermissionDenied'))
    else:
        form = UserCreatingForm()
    return render(request, "sign_up_page.html", {'form': form})


def update_group_view(request, group_id):
    group = Group.objects.filter(id=group_id).first()
    if request.method == 'POST':
        form = GroupCreatingForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('list_of_groups')
    elif request.method == 'POST' and not request.user.is_superuser:
        raise ValidationError(_('PermissionDenied'))
    else:
        form = GroupCreatingForm(instance=group)

    return render(request, "group_update_page.html", {'form': form})


def update_user_view(request, user_id):
    user = User.objects.filter(id=user_id).first()
    if request.method == 'POST':
        form = UserCreatingForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('list_of_groups')
    elif request.method == 'POST' and not request.user.is_superuser:
        raise ValidationError(_('PermissionDenied'))
    else:
        form = UserCreatingForm(instance=user)

    return render(request, "sign_up_page.html", {'form': form})
