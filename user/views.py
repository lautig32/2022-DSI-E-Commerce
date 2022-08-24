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
        university_name = request.POST.get('university_name')
        university_id = request.POST.get('university_id')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        data = {'first_name': fname, 'last_name': lname, 'email': email, 'document_number': document_number,
                'password2': password2, 'password1': password1}
        form = SignUpForm(data=data)
        if form.is_valid():
            user = form.save(commit=False)

            user.is_active = False
            user.is_staff = True
            user.user_type = UserProfile.SUBSCRIBER
            user.save()

            admin_group_user = Group.objects.get(name=user.user_type)
            admin_group_user.user_set.add(user.pk)
            admin_group_user.save()

            current_site = get_current_site(request)
            subject = 'Jornadas de Ciencia y Tecnología 2022: Confirmación de cuenta'
            message = render_to_string('persons/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            user.email_user(subject, message)

            return HttpResponse(json.dumps({"message": "Success"}), content_type="application/json")

        else:
            return HttpResponse(json.dumps({"message": form.errors}), content_type="application/json")
    else:
        form = SignUpForm()
        return render(request, 'persons/signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'persons/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserProfile.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserProfile.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_staff = True
        user.save()
        admin_group_user = Group.objects.get(name=user.user_type)
        admin_group_user.user_set.add(user.pk)
        admin_group_user.save()
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'persons/account_activation_invalid.html')
