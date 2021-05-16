from django.forms import ModelForm
from apps.artwork.models import Artwork


class ArtworkForm(ModelForm):
    class Meta:
        model = Artwork
        fields = ['category', 'image', 'title', 'description', 'price']