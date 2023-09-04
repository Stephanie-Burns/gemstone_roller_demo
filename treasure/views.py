
from django.db import transaction
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, render, redirect

from . import forms
from . import models
from . import services


def index(request):
    return render(request, 'treasure/index.html')


def gemstone_index(request):
    gemstones = models.Gemstone.objects.all()
    return render(request, 'treasure/gemstone-index.html', {'gemstones': gemstones})


@transaction.atomic
def gemstone_create(request):

    if request.method == 'POST':

        form = forms.GemstoneForm(request.POST, request.FILES)

        if form.is_valid():

            gemstone = form.save(commit=False)
            upload_icon = request.FILES.get('icon', None)
            gemstone.icon = services.get_or_create_icon(upload_icon, gemstone.name)
            gemstone.save()

            return redirect('treasure:gemstone_index')

    else:

        form = forms.GemstoneForm()
        default_icon_url = models.GemstoneIcon.objects.get(id=1).image.url

    return render(request, 'treasure/gemstone-create.html', {'form': form, 'icon_url': default_icon_url})


def gemstone_view(request, gemstone_id):
    gemstone = get_object_or_404(models.Gemstone, pk=gemstone_id)
    return render(request, 'treasure/gemstone-view.html', {'gemstone': gemstone})


@transaction.atomic
def gemstone_edit(request, gemstone_id):
    gemstone = get_object_or_404(models.Gemstone, pk=gemstone_id)

    if request.method == 'POST':
        form = forms.GemstoneForm(request.POST, instance=gemstone)

        if form.is_valid():
            gemstone = form.save(commit=False)
            upload_icon = request.FILES.get('icon', None)

            if upload_icon:
                gemstone.icon = services.get_or_create_icon(upload_icon, gemstone.name)

            gemstone.save()
            return redirect('treasure:gemstone_index')

    else:
        form = forms.GemstoneForm(instance=gemstone)

    icon_url = gemstone.icon.image.url if gemstone.icon else None
    context = {'form': form, 'icon_url': icon_url, 'gemstone_id': gemstone_id}
    return render(request, 'treasure/gemstone-edit.html', context)


def gemstone_delete(request, gemstone_id):

    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    gemstone = get_object_or_404(models.Gemstone, pk=gemstone_id)
    gemstone.delete()

    return redirect('treasure:gemstone_index')


def gemstone_all(request):
    gemstones = models.Gemstone.objects.all()
    return render(request, 'treasure/gemstone-all.html', {'gemstones': gemstones})
