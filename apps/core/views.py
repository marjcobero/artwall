from django.shortcuts import render
from apps.artwork.models import Artwork


# Create your views here.


def frontpage(request):
    newest_artworks = Artwork.objects.all()[0:8]
    return render(request, 'core/frontpage.html', {'newest_artworks': newest_artworks})
