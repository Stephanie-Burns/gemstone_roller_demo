
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.text import slugify

from . import forms
from . import models
from . import services


def index(request):
    return render(request, 'treasure/index.html')


def gemstone_create(request):

    if request.method == 'POST':

        form = forms.GemstoneForm(request.POST, request.FILES)

        if form.is_valid():

            with transaction.atomic():

                gemstone = form.save(commit=False)
                upload_icon = request.FILES.get('icon', None)
                gemstone.icon = services.get_or_create_icon(upload_icon, gemstone.name)
                gemstone.save()

            return redirect('treasure:index')

    else:

        form = forms.GemstoneForm()

    return render(request, 'treasure/gemstone-create.html', {'form': form})


def gemstone_all(request):
    gemstones = models.Gemstone.objects.all()
    return render(request, 'treasure/gemstone-all.html', {'gemstones': gemstones})
