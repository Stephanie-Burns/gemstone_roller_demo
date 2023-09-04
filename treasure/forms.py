
from django import forms
from . import models


class GemstoneForm(forms.ModelForm):

    icon = forms.ImageField(widget=forms.FileInput, required=False)

    class Meta:

        model = models.Gemstone
        fields = ['name', 'description', 'value']

    def clean_icon(self):

        icon = self.cleaned_data.get('icon')
        if icon:

            if icon.size > 2 * 1024 * 1024:  # Limit to 5 MB

                raise forms.ValidationError('File size must be no more than 2 MB.')

        return icon
