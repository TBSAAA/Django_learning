

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django_redis import get_redis_connection


from web import models

from utils.ajax_response import BaseResponse

from web.forms.account import LoginForm, mobileLoginForm, MobileForm


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

        # 2. check data   1. admin  2. customer
        if role == '1':
            user_object = models.Administrator.objects.filter(active=1, username=username, password=password).first()
        else:
            user_object = models.Customer.objects.filter(active=1, username=username, password=password).first()

        # 3. check result
        # 3.1 check failed
        if not user_object:
            return render(request, 'login.html', {'error': 'user or password error', 'form': form})

        # 3.2 check success --> write session and redirect
        mapping = {'1': 'ADMIN', '2': 'CUSTOMER'}
        request.session['user_info'] = {'role': mapping[role], 'name': user_object.username, 'id': user_object.id}
        return redirect('/index/')


def login_message(request):
    if request.method == 'GET':
        mobileForms = mobileLoginForm()
        return render(request, 'login_message.html', {'forms': mobileForms})
    else:
        res = BaseResponse()
        # 1. check mobile number is correct or not
        mobileForms = mobileLoginForm(data=request.POST)
        if not mobileForms.is_valid():
            res.error = mobileForms.errors
            return JsonResponse(res.dict)

        role = mobileForms.cleaned_data.get('role')
        mobile = mobileForms.cleaned_data.get('mobile')

        if role == '1':
            user_object = models.Administrator.objects.filter(active=1, mobile=mobile).first()
        else:
            user_object = models.Customer.objects.filter(active=1, mobile=mobile).first()
        if not user_object:
            res.error = {'mobile': 'mobile number is not exist'}
            return JsonResponse(res.dict)
        mapping = {'1': 'ADMIN', '2': 'CUSTOMER'}
        request.session['user_info'] = {'role': mapping[role], 'name': user_object.username, 'id': user_object.id}
        res.status = True
        res.data = '/index/'
        return JsonResponse(res.dict)


def send_code(request):
    res = BaseResponse()
    # check phone number + role
    form = MobileForm(data=request.POST)
    if not form.is_valid():
        res.error = form.errors
        return JsonResponse(res.dict)
    else:
        res.status = True
        return JsonResponse(res.dict)

