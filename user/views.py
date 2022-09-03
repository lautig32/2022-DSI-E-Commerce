import json

from django.contrib.auth import logout as do_logout, authenticate, login
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import UpdateView
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from user.forms import *


def home(request):
    return render(request, 'user/home.html')


def my_profile(request):
    form = EditMyProfileForm(request.POST)
    user = request.user
    url_domain = get_current_site(request).domain
    context = {
                'form': form,
                'user': user,
                'url_domain': url_domain,
                }
    if request.method == 'GET':
        return render(request, 'user/profile.html', context)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.document_number = request.POST.get('document_number')
        user.address = request.POST.get('address')
        user.number_adress = request.POST.get('number_adress')
        user.number_phone = request.POST.get('number_phone')
        user.is_active = True
        user.save()
        return HttpResponseRedirect(reverse('profile'))
    return render(request, 'user/profile.html', context)


def logout(request):
    do_logout(request)
    return HttpResponseRedirect(reverse('home'))


def user_login(request):
    if request.method == 'GET':
        return render(request, 'user/login.html')
    if request.method == 'POST':
        email = request.POST.get('email').strip()
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('profile'))
            else:
                return HttpResponse(json.dumps({"message": "inactive"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"message": "invalid"}), content_type="application/json")
    else:
        form = SignUpForm(request.POST)
        return render(request, 'user/register.html', {'form': form})


def register(request):
    form = SignUpForm(request.POST)
    context = {
                'form': form
                }
    if request.method == "POST":
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        email = request.POST.get('email')
        document_number = request.POST.get('document_number')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        address = request.POST.get('address')
        number_adress = request.POST.get('number_adress')
        number_phone = request.POST.get('number_phone')
        data = {'first_name': fname, 'last_name': lname, 'email': email, 'document_number': document_number,
                'password2': password2, 'password1': password1,
                'address': address, 'number_adress': number_adress, 'number_phone': number_phone}
        form = SignUpForm(data=data)
        """form = SignUpForm(request.POST)"""
        context = {
                'form': form
                }
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.is_staff = True
            user.save()
            return HttpResponseRedirect(reverse('profile'))
        else:
            return render(request, "user/register.html", context)
    else:
        return render(request, 'user/register.html', context)


def favorite(request):
    return render(request, 'user/favorite.html')