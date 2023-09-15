
import random

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
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

    if request.method == 'POST':

        form = forms.GemstoneForm(request.POST, request.FILES)

        if form.is_valid():

            gemstone = form.save(commit=False)
            upload_icon = request.FILES.get('icon', None)
            gemstone.icon = services.get_or_create_icon(upload_icon, gemstone.name)
            gemstone.created_by = request.user
            gemstone.save()

            return redirect('treasure:gemstone_view', gemstone.id)

    else:

        form = forms.GemstoneForm()

    return render(request, 'treasure/gemstone-create.html', {'form': form})


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
    htmx_request = request.headers.get('HX-Request')

    if request.method == 'POST':
        form = forms.GemstoneForm(request.POST, instance=gemstone)

        if form.is_valid():
            gemstone = form.save(commit=False)
            upload_icon = request.FILES.get('icon', None)

            if upload_icon:
                gemstone.icon = services.get_or_create_icon(upload_icon, gemstone.name)

            gemstone.save()
            return HttpResponseRedirect(reverse('gemstone_view', args=[gemstone.id]))

    if request.method == 'GET':

        form = forms.GemstoneForm(instance=gemstone)
        icon_url = gemstone.icon.image.url if gemstone.icon else None
        context = {'form': form, 'icon_url': icon_url, 'gemstone_id': gemstone_id}

        if htmx_request:
            template = 'treasure/snippets/gemstone-form.html'
            context['modal_view'] = True

        else:
            template = 'treasure/gemstone-edit.html'

        return render(request, template, context)


@login_required
def gemstone_delete(request, gemstone_id):

    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    gemstone = get_object_or_404(models.Gemstone, pk=gemstone_id)
    gemstone.delete()

    response = HttpResponse()
    response["HX-Redirect"] = request.build_absolute_uri(reverse('treasure:gemstone_search'))
    return response


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

    if request.headers.get('HX-Request'):
        return render(request, 'treasure/snippets/gemstone-form.html', {'form': form})
    else:
        return render(request, 'treasure/gemstone-create.html', {'form': form})
