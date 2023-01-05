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
from django.views.generic import UpdateView, View, TemplateView, FormView, CreateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from .models import UserProfile
from .forms import *


# TODO: metodo para recuperar la clave con pregunta secreta


def get_url_domain(request):

    return get_current_site(request).domain


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
    if 'update_profile' in request.POST:
        return render(request, 'user/update_profile.html', context)
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


class UserLoginView(View):
    model = UserProfile
    template_name = 'user/profile.html'
    form_class = UserProfileAuthenticationForm
    success_url = reverse_lazy('user:profile')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)

    def get(self, request, *args, **kwargs):
        form = UserProfileAuthenticationForm()
        context = {
                    'form': form,
                    'url_domain': get_url_domain(request),
                }
        return render(request, 'user/login.html', context)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('username').strip()
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('user:profile'))
            else:
                return HttpResponseRedirect(reverse('user:login'))
        else:
            return HttpResponseRedirect(reverse('user:login'))

class LogoutTemplateView(TemplateView):

    def get(self, request, *args, **kwargs):
        do_logout(request)
        return HttpResponseRedirect(reverse('user:login'))


class UserProfileUpdateView(UpdateView): # TODO: ver 
    model = UserProfile
    template_name = 'user/update_profile.html'
    form_class = EditMyProfileForm
    success_url = reverse_lazy('user:update_profile')

    def get(self, request, *args, **kwargs):
        form = EditMyProfileForm()
        user = request.user
        url_domain = get_current_site(request).domain
        context = {
                    'form': form,
                    'user': user,
                    'url_domain': url_domain,
                    }
        return render(request, 'user/profile.html', context)

    def post(self, request, *args, **kwargs):
        form = EditMyProfileForm()
        user = request.user
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

        context = {
                    'form': form,
                    'user': user,
                    'url_domain': get_url_domain(request),
        }

        return render(request, 'user/profile.html', context)



class UserProfileCreateView(CreateView):
    model = UserProfile
    template_name = "user/register.html"
    form_class = UserProfileForm
    success_url = reverse_lazy("user: profile")

    def post(self, request, *args, **kwargs):
        # first_name = request.POST.get('first_name')
        # last_name = request.POST.get('last_name')
        # document_number = request.POST.get('document_number')
        # number_phone = request.POST.get('number_phone')
        # address = request.POST.get('address')
        # number_adress = request.POST.get('number_adress')
        # email = request.POST.get('email')
        # password1 = request.POST.get('password1')
        # password2 = request.POST.get('password2')
        # data = {'first_name': first_name, 'last_name': last_name, 'email': email, 'document_number': document_number,
        #         'password2': password2, 'password1': password1,
        #         'address': address, 'number_adress': number_adress, 'number_phone': number_phone}
        form = UserProfileForm(data=request.POST)
        context = {
                'form': form,
                'url_domain': get_url_domain(request),
            }
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.is_staff = False
            user.save()
            user = authenticate(username=user.email, password=user.password)
            login(request, user)
            return HttpResponseRedirect(reverse('user:profile'))
        else:
            return render(request, "user/register.html", context)


# def register(request):
#     url_domain = get_current_site(request).domain
#     form = UserProfileForm()
#     context = {
#                 'form': form,
#                 'url_domain': url_domain,
#             }
#     if request.method == "GET":
#         return render(request, 'user/register.html', context)
#     if request.method == "POST":
#         fname = request.POST.get('first_name')
#         lname = request.POST.get('last_name')
#         document_number = request.POST.get('document_number')
#         number_phone = request.POST.get('number_phone')
#         address = request.POST.get('address')
#         number_adress = request.POST.get('number_adress')
#         email = request.POST.get('email')
#         password1 = request.POST.get('password1')
#         password2 = request.POST.get('password2')
#         data = {'first_name': fname, 'last_name': lname, 'email': email, 'document_number': document_number,
#                 'password2': password2, 'password1': password1,
#                 'address': address, 'number_adress': number_adress, 'number_phone': number_phone}
#         form = UserProfileForm(data=data)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = True
#             user.is_staff = False
#             user.save()
#             user = authenticate(username=email, password=password1)
#             login(request, user)
#             return HttpResponseRedirect(reverse('profile'))
#         else:
#             return render(request, "user/register.html", context)
#     else:
#         return render(request, 'user/register.html', context)
