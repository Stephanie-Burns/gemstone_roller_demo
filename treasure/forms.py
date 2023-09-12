
from django import forms

from . import models


DESCRIPTION_PLACEHOLDER = (
    "The Wyrmfire Topaz is a gemstone unlike any other, glowing with an "
    "ever-changing dance of flames trapped within its transparent core. "
    "Its iridescent hue shifts from a fiery orange to a deep crimson, mimicking "
    "the intensity of a dragon's breath. Legends say this topaz was born from "
    "the tears of ancient wyrms, imbuing it with arcane energies. "
    "\n\n"
    "Whoever possesses this mystical stone is said to gain a mastery over "
    "elemental fire, granting them an indomitable spirit and unparalleled "
    "courage. Warriors and mages alike seek the Wyrmfire Topaz, for it not "
    "only ignites the mind but also empowers spells of fire and destruction. "
    "It's a gemstone that is as volatile as it is mesmerizing, a true "
    "embodiment of the untamable forces of the world."
)


class GemstoneForm(forms.ModelForm):

    class Meta:

        model = models.Gemstone
        fields = ['name', 'clarity', 'color', 'description', 'value']

    icon = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'gemstone-file-input', 'id': 'gemstone-icon-upload'}),
        required=False
    )
    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'gemstone-form-text-input-lg', 'placeholder': 'Wyrmfire Topaz'})
    )
    color = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'gemstone-from-text-input', 'placeholder': 'Fiery orange to deep crimson'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'gemstone-form-textarea-input', 'placeholder': DESCRIPTION_PLACEHOLDER}),
    )

    def clean_icon(self):

        icon = self.cleaned_data.get('icon')
        if icon:

            if icon.size > 2 * 1024 * 1024:  # Limit to 2 MB

                raise forms.ValidationError('File size must be no more than 2 MB.')

        return icon
