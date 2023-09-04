
from django import forms
from . import models


class GemstoneForm(forms.ModelForm):

    icon = forms.ImageField(widget=forms.FileInput, required=False)

    class Meta:
        model = models.Gemstone
        fields = ['name', 'description', 'value']