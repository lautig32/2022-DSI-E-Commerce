import json

from django.contrib.auth import logout as do_logout, authenticate, login
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from user.forms import SignUpForm
from user.models import UserProfile

def home(request):
    return render(request, 'user/login.html')


def my_profile(request):
    return render(request, 'user/profile.html')

def register(request):
    return render(request, 'user/register.html')


def logout(request):
    do_logout(request)
    return HttpResponseRedirect(reverse('index'))


def user_login(request):
    if request.method == 'GET':
        return render(request, 'persons/login.html')
    if request.method == 'POST':
        email = request.POST.get('email').strip()
        password = request.POST.get('password')

        user = authenticate(username=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse(json.dumps({"message": "Success"}), content_type="application/json")

            else:
                return HttpResponse(json.dumps({"message": "inactive"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"message": "invalid"}), content_type="application/json")

        # return HttpResponse(json.dumps({"message": "denied"}),content_type="application/json")

    else:
        return HttpResponseRedirect(reverse('index'))


def signup(request):
    if request.method == 'POST':
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        email = request.POST.get('email').strip()
        document_number = request.POST.get('document_number')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        address = request.POST.get('address')
        number_address = request.POST.get('number_address')
        number_phone = request.POST.get('number_phone')

        data = {'first_name': fname, 'last_name': lname, 'email': email, 'document_number': document_number,
                'password2': password2, 'password1': password1, 'address': address,
                'number_address': number_address, 'number_phone': number_phone}

        form = SignUpForm(data=data)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.is_staff = True
            user.save()
            return HttpResponse(json.dumps({"message": "Success"}), content_type="application/json")

        else:
            return HttpResponse(json.dumps({"message": form.errors}), content_type="application/json")
    else:
        form = SignUpForm()
        return render(request, 'persons/signup.html', {'form': form})