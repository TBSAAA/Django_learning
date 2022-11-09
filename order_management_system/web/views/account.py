from django.shortcuts import render, redirect, HttpResponse
from web import models
from utils.encrypt import md5

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        # 1. get data
        username = request.POST.get('username')
        password = request.POST.get('password')
        password = md5(password)
        role = request.POST.get('role')
        # 2. check data   1. admin  2. customer
        mapping = {'1': 'ADMIN', '2': 'CUSTOMER'}
        if role not in mapping:
            return render(request, 'login.html', {'error': 'role not exist'})
        if role == '1':
            user_object = models.Administrator.objects.filter(active=1, username=username, password=password).first()
        else:
            user_object = models.Customer.objects.filter(active=1, username=username, password=password).first()
        # 3. check result
        # 3.1 check failed
        if not user_object:
            return render(request, 'login.html', {'error': 'user or password error'})
        # 3.2 check success --> write session and redirect
        request.session['user_info'] = {'role': mapping[role], 'name': user_object.username, 'id': user_object.id}
        return redirect('/index/')


def login_message(request):
    if request.method == 'GET':
        return render(request, 'login_message.html')
    else:
        print(request.POST)
        return render(request, 'login_message.html')
