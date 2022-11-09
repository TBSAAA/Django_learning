from django.shortcuts import render, redirect, HttpResponse


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        print(request.POST)


def login_message(request):
    if request.method == 'GET':
        return render(request, 'login_message.html')
    else:
        print(request.POST)
