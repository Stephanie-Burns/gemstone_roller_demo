
import random

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from . import forms
from . import models
from . import services


def index(request):
    return render(request, 'treasure/index.html')


def gemstone_index(request):
    gemstones = models.Gemstone.objects.all().order_by(models.GEMSTONE_DEFAULT_ORDER)
    return render(request, 'treasure/gemstone-index.html', {'gemstones': gemstones})


@login_required
@transaction.atomic
def gemstone_create(request):

    default_icon_url = models.GemstoneIcon.objects.get(id=1).image.url
    
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

    context = {'form': form, 'icon_url': default_icon_url}
    return render(request, 'treasure/gemstone-create.html', context)


def gemstone_view(request, gemstone_id):

    context = {'gemstone': get_object_or_404(models.Gemstone, pk=gemstone_id), 'is_htmx': False}

    if request.headers.get('HX-Request'):
        context['htmx_request'] = True
        return render(request, 'treasure/snippets/gemstone-data.html', context)

    else:
        return render(request, 'treasure/gemstone-view.html', context)


@login_required
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


@login_required
def gemstone_delete(request, gemstone_id):

    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    gemstone = get_object_or_404(models.Gemstone, pk=gemstone_id)
    gemstone.delete()

    return redirect('treasure:gemstone_index')


def gemstone_all(request):
    gemstones = models.Gemstone.objects.all().order_by(models.GEMSTONE_DEFAULT_ORDER)
    return render(request, 'treasure/snippets/gemstone-all.html', {'gemstones': gemstones})


def gemstone_search(request):
    gemstones = models.Gemstone.objects.all().order_by(models.GEMSTONE_DEFAULT_ORDER)
    return render(request, 'treasure/gemstone-search.html', {'gemstones': gemstones})


def gemstone_roll(request):

    if request.headers.get('HX-Request'):

        gemstones = []
        for gem, count in request.GET.items():

            if gem.startswith('gem') and int(count) > 0:

                gem_objects = (
                    models.Gemstone.objects
                    .filter(value__exact=gem.split('-')[1])
                    .order_by(models.GEMSTONE_DEFAULT_ORDER)
                )
                gemstones.extend(random.choices(gem_objects, k=int(count)))

        return render(request, 'treasure/snippets/gemstone-table.html', {'gemstones': gemstones})

    return render(request, 'treasure/gemstone-roll.html')


# ========================= HTMX endpoints
def gemstone_search_table(request):

    # TODO const dict and function(...EXPECTED_REFERER, redirect_url)
    referer = request.headers.get('Referer')
    expected_referer = request.build_absolute_uri(reverse('treasure:gemstone_search'))
    htmx_request = request.headers.get('HX-Request')

    if referer != expected_referer or not htmx_request:
        return redirect('treasure:gemstone_search')

    context = {'gemstones': None, 'search_enabled': True}
    search_term = request.GET.get('q')

    if search_term:

        context['gemstones'] = (
            models.Gemstone.objects
            .search_for(search_term=search_term)
            .order_by(models.GEMSTONE_DEFAULT_ORDER)
        )

        return render(request, 'treasure/snippets/gemstone-table.html', context)

    else:
        context['gemstones'] = models.Gemstone.objects.all().order_by(models.GEMSTONE_DEFAULT_ORDER)
        return render(request, 'treasure/snippets/gemstone-table.html', context)


def gemstone_form(request):

    gem_id = request.GET.get('id')

    if gem_id:
        gemstone = get_object_or_404(models.Gemstone, pk=gem_id)
        form = forms.GemstoneForm(instance=gemstone)
    else:
        form = forms.GemstoneForm()

    return render(request, 'treasure/snippets/gemstone-form.html', {'form': form})
