
import random

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from . import forms
from . import models
from . import services


def index(request):
    return render(request, 'treasure/index.html')


def gemstone_index(request):
    user = services.get_user(request)
    gemstones = models.Gemstone.objects.base_queryset(user=user)

    return render(request, 'treasure/gemstone-index.html', {'gemstones': gemstones})


@login_required
@transaction.atomic
def gemstone_create(request):

    if request.method == 'POST':

        form = forms.GemstoneForm(request.POST, request.FILES)

        if form.is_valid():

            gemstone = form.save(commit=False)
            upload_icon = request.FILES.get('icon', None)
            gemstone.icon = services.get_or_create_icon(upload_icon, gemstone.name, request.user)
            gemstone.created_by = request.user
            gemstone.save()

            return redirect('treasure:gemstone_view', gemstone.id)

        else:
            return render(request, 'treasure/gemstone-create.html', {'form': form})

    else:

        form = forms.GemstoneForm()

    return render(request, 'treasure/gemstone-create.html', {'form': form})


def gemstone_view(request, gemstone_id):

    modal_view = services.is_modal_view(request)
    context = {'gemstone': get_object_or_404(models.Gemstone, pk=gemstone_id), 'modal': modal_view}

    if modal_view:
        return render(request, 'treasure/snippets/gemstone-data.html', context)

    return render(request, 'treasure/gemstone-view.html', context)


@login_required
@services.user_owns_gemstone
@transaction.atomic
def gemstone_edit(request, gemstone_id):

    gemstone = request.gemstone
    modal_view = services.is_modal_view(request)

    if request.method == 'POST':
        form = forms.GemstoneForm(request.POST, instance=gemstone)

        if form.is_valid():
            gemstone = form.save(commit=False)
            upload_icon = request.FILES.get('icon', None)

            if upload_icon:
                gemstone.icon = services.get_or_create_icon(upload_icon, gemstone.name, request.user)

            gemstone.save()

            context = {"gemstone": gemstone, 'modal': modal_view}

            if modal_view:

                return render(request, 'treasure/snippets/gemstone-data.html', context)

            return render(request, 'treasure/gemstone-view.html', context)

        else:  # Form Invalid

            icon_url = gemstone.icon.image.url if gemstone.icon else None
            context = {'form': form, 'icon_url': icon_url, 'gemstone_id': gemstone_id, 'modal': modal_view}

            if modal_view:
                return render(request, 'treasure/snippets/gemstone-form.html', context)

            return render(request, 'treasure/gemstone-edit.html', context)

    if request.method == 'GET':

        form = forms.GemstoneForm(instance=gemstone)
        icon_url = gemstone.icon.image.url if gemstone.icon else None
        context = {'form': form, 'icon_url': icon_url, 'gemstone_id': gemstone_id, 'modal': modal_view}
        print(modal_view)

        if modal_view:
            return render(request, 'treasure/snippets/gemstone-form.html', context)

        return render(request, 'treasure/gemstone-edit.html', context)


@login_required
@services.user_owns_gemstone
def gemstone_delete(request, gemstone_id):

    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    gemstone = request.gemstone
    gemstone.delete()

    return services.htmx_redirect(request, 'treasure:gemstone_search')


def gemstone_all(request):

    user = services.get_user(request)
    gemstones = models.Gemstone.objects.base_queryset(user=user)

    return render(request, 'treasure/snippets/gemstone-all.html', {'gemstones': gemstones})


def gemstone_search(request):

    user = services.get_user(request)
    gemstones = models.Gemstone.objects.base_queryset(user=user)

    return render(request, 'treasure/gemstone-search.html', {'gemstones': gemstones})


def gemstone_roll(request):

    if request.headers.get('HX-Request'):

        user = services.get_user(request)
        gem_pool = models.Gemstone.objects.base_queryset(user=user)

        gemstones = []

        for gem, count in request.GET.items():

            # TODO scrub this against list for security
            if gem.startswith('gem') and int(count) > 0:

                gem_objects = gem_pool.filter(value__exact=gem.split('-')[1])
                gemstones.extend(random.choices(gem_objects, k=int(count)))

        return render(request, 'treasure/snippets/gemstone-table.html', {'gemstones': gemstones})

    return render(request, 'treasure/gemstone-roll.html')


# HTMX endpoints =============================================================
def gemstone_search_table(request):

    if not request.headers.get('HX-Request'):
        return redirect('treasure:gemstone_search')

    if request.method == 'POST':

        context = {'search_enabled': True}
        search_term = request.POST.get('q')

        user = services.get_user(request)
        gem_pool = models.Gemstone.objects.search_for(search_term=search_term, user=user)

        context['gemstones'] = services.apply_search_filters(request, gem_pool)

        return render(request, 'treasure/snippets/gemstone-table.html', context)


@login_required()
def gemstone_form(request):
    form = forms.GemstoneForm()
    return render(request, 'treasure/snippets/gemstone-form.html', {'form': form})
