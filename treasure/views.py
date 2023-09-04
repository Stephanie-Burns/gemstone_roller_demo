
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
                # upload_icon = request.FILES.get('icon', None)
                upload_icon = form.icon

                if upload_icon:
                    file_hash = services.calculate_file_hash(upload_icon)

                    existing_icon = models.GemstoneIcon.objects.filter(file_hash=file_hash).first()
                    if existing_icon:
                        gemstone.icon = existing_icon

                    else:
                        new_icon = models.GemstoneIcon.objects.create(image=upload_icon, file_hash=file_hash)
                        new_icon.generate_name(gemstone.name, file_hash)
                        new_icon.save()
                        gemstone.icon = new_icon
                else:
                    default_icon = models.GemstoneIcon.objects.get(id=1)
                    gemstone.icon = default_icon

                gemstone.save()

            return redirect('treasure:index')

    form = forms.GemstoneForm()
    return render(request, 'treasure/gemstone-create.html', {'form': form})

def gemstone_all(request):
    gemstones = models.Gemstone.objects.all()
    return render(request, 'treasure/gemstone-all.html', {'gemstones': gemstones})