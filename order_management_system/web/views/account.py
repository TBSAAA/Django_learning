from django.shortcuts import render, redirect, HttpResponse
from web import models
from utils.encrypt import md5
from django import forms
import random
from scripts import send_sms
from django.http import JsonResponse
from django_redis import get_redis_connection


class LoginForm(forms.Form):
    role = forms.ChoiceField(
        required=True,
        choices=(("2", "user"), ("1", "admin")),
        widget=forms.Select(attrs={"class": "form-control"}),
        error_messages={'required': 'role is required'}
    )
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "username"}),
        error_messages={'required': 'username is required'}
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "password"}, render_value=True),
        error_messages={'required': 'password is required'}
    )


class mobileLoginForm(forms.Form):
    role = forms.ChoiceField(
        required=True,
        choices=(("2", "user"), ("1", "admin")),
        widget=forms.Select(attrs={"class": "form-control"}),
        error_messages={'required': 'role is required'}
    )
    mobile = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "mobile", "id": "mobile"}),
        error_messages={'required': 'mobile is required'}
    )
    code = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "code"}),
        error_messages={'required': 'code is required'}
    )


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    else:
        # 1. get data and check data is empty
        form = LoginForm(data=request.POST)
        if not form.is_valid():
            return render(request, 'login.html', {'form': form})
        role = form.cleaned_data.get('role')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        password = md5(password)

        # 2. check data   1. admin  2. customer
        mapping = {'1': 'ADMIN', '2': 'CUSTOMER'}
        if role not in mapping:
            return render(request, 'login.html', {'error': 'role not exist', 'form': form})
        if role == '1':
            user_object = models.Administrator.objects.filter(active=1, username=username, password=password).first()
        else:
            user_object = models.Customer.objects.filter(active=1, username=username, password=password).first()

        # 3. check result
        # 3.1 check failed
        if not user_object:
            return render(request, 'login.html', {'error': 'user or password error', 'form': form})

        # 3.2 check success --> write session and redirect
        request.session['user_info'] = {'role': mapping[role], 'name': user_object.username, 'id': user_object.id}
        return redirect('/index/')


def login_message(request):
    if request.method == 'GET':
        mobileForms = mobileLoginForm()
        return render(request, 'login_message.html', {'forms': mobileForms})
    else:
        mobileForms = mobileLoginForm(data=request.POST)
        if not mobileForms.is_valid():
            return render(request, 'login_message.html', {'forms': mobileForms})
        role = mobileForms.cleaned_data.get('role')
        mobile = mobileForms.cleaned_data.get('mobile')
        code = mobileForms.cleaned_data.get('code')
        conn = get_redis_connection("default")
        if code != conn.get(mobile).decode():
            return render(request, 'login_message.html', {'forms': mobileForms, 'error': 'code error'})
        mapping = {'1': 'ADMIN', '2': 'CUSTOMER'}
        if role not in mapping:
            return render(request, 'login_message.html', {'forms': mobileForms, 'error': 'role error'})
        if role == '1':
            user_object = models.Administrator.objects.filter(active=1, mobile=mobile).first()
        else:
            user_object = models.Customer.objects.filter(active=1, mobile=mobile).first()
        if not user_object:
            return render(request, 'login_message.html', {'forms': mobileForms, 'error': 'user not exist'})
        request.session['user_info'] = {'role': mapping[role], 'name': user_object.username, 'id': user_object.id}
        return redirect('/index/')


def send_code(request):
    # check phone number
    phone = request.POST.get('phone_number')
    print(phone)
    if not phone:
        return JsonResponse({'status': False, 'error': 'phone number is empty'})
    # random code
    code = random.randint(1000, 9999)

    # send code
    # v_code = send_sms.send_sms(phone, code)
    # if v_code:
    conn = get_redis_connection("default")
    conn.set(phone, code, ex=60)
    #     return JsonResponse({'status': True, 'code': code})
    # else:
    #     return JsonResponse({'status': False, 'error': 'send code failed, please try again'})

    return JsonResponse({'status': True, 'code': code})
