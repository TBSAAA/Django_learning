from django.shortcuts import render, redirect, HttpResponse
from web import models
from utils.encrypt import md5
from django import forms


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
        return render(request, 'login_message.html')
    else:
        print(request.POST)
        return render(request, 'login_message.html')

# old version
# def login(request):
#     if request.method == 'GET':
#         return render(request, 'login.html')
#     else:
#         # 1. get data and check data is empty
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         password = md5(password)
#         role = request.POST.get('role')
#         # 2. check data   1. admin  2. customer
#         mapping = {'1': 'ADMIN', '2': 'CUSTOMER'}
#         if role not in mapping:
#             return render(request, 'login.html', {'error': 'role not exist'})
#         if role == '1':
#             user_object = models.Administrator.objects.filter(active=1, username=username, password=password).first()
#         else:
#             user_object = models.Customer.objects.filter(active=1, username=username, password=password).first()
#         # 3. check result
#         # 3.1 check failed
#         if not user_object:
#             return render(request, 'login.html', {'error': 'user or password error'})
#         # 3.2 check success --> write session and redirect
#         request.session['user_info'] = {'role': mapping[role], 'name': user_object.username, 'id': user_object.id}
#         return redirect('/index/')
