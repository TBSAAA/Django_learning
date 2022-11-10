from django.shortcuts import render, redirect, HttpResponse
from web import models
from django import forms
from django.urls import reverse


class LevelForm(forms.Form):
    title = forms.CharField(
        label="title",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "title"}),
        error_messages={'required': 'title is required'},
    )
    percent = forms.CharField(
        label="discount",
        required=True,
        help_text="Fill in an integer from 0-100 to indicate a percentage, for example: 90, indicates 90%",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "discount"}),
        error_messages={'required': 'discount is required'},
    )


def level_list(request):
    levels = models.Level.objects.filter(active=1)
    form = LevelForm()
    return render(request, 'level_list.html', {"levels": levels}, {"form": form})


def level_add(request):
    if request.method == "GET":
        form = LevelForm()
        return render(request, 'level_add.html', {"form": form})
    else:
        form = LevelForm(data=request.POST)
        if not form.is_valid():
            return render(request, 'level_add.html', {"form": form})
        title = form.cleaned_data.get('title')
        percent = form.cleaned_data.get('percent')
        # add to database
        models.Level.objects.create(title=title, percent=percent)
        return redirect(reverse('level_list'))


def level_edit(request, pk):
    pass


def level_delete(request, pk):
    pass
