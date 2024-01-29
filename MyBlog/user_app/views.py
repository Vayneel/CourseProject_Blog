from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from user_app.forms import *
from user_app.models import *


def auth(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('main_page'))
    if request.method == 'POST':
        form = UserAuthForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                logout(request)
                login(request, user)
                return HttpResponseRedirect(reverse('main_page'))
        return HttpResponseRedirect(reverse('auth'))
    form = UserAuthForm()
    return render(request, 'user_app/auth.html', {'form': form})


def reg(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('main_page'))
    if request.method == 'POST':
        form = UserRegForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserAdditional.objects.create(linked_user=user)
            logout(request)
            login(request, user)
            return HttpResponseRedirect(reverse('main_page'))
        return HttpResponseRedirect(reverse('reg'))
    form = UserRegForm()
    return render(request, 'user_app/reg.html', {'form': form})


@login_required
def lout(request):
    logout(request)
    return HttpResponseRedirect(reverse('main_page'))


@login_required
def user_profile(request):
    user_add = UserAdditional.objects.get(linked_user=request.user)
    if request.method == 'POST':
        form = UserAdditionalForm(request.POST)
        if form.is_valid():
            form_to_save = form.save(commit=False)
            user_add.avatar = form_to_save.avatar
            user_add.birthday = form_to_save.birthday
            user_add.save()
            if request.POST.get('redir'):
                return HttpResponseRedirect(reverse('user_profile'))
        return render(request, 'user_app/user_profile.html', {'user': request.user, 'user_add': user_add,
                                                              'is_authenticated': True,
                                                              'change': request.POST.get('change'), 'form': form})
    return render(request, 'user_app/user_profile.html', {'user': request.user, 'user_add': user_add,
                                                          'is_authenticated': True, 'change': False})


# todo: show errors, that occur during reg or auth
# todo error messages
# todo paging (10 posts on page)
