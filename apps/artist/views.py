from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.utils.text import slugify

from .models import Artist
from apps.artwork.models import Artwork
from .forms import ArtworkForm


# Create your views here.


def join(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            artist = Artist.objects.create(
                name=user.username, 
                created_by=user
                )
            return redirect('frontpage')
    else:
        form = UserCreationForm()
    return render(request, 'artist/join.html', {'form': form})

@login_required
def artist_admin(request):
    artist = request.user.artist
    artworks = artist.artworks.all()
    orders = artist.orders.all()
    for order in orders:
        order.artist_amount = 0
        order.artist_paid_amount = 0
        order.fully_paid = True
        for item in order.items.all():
            if item.artist == request.user.artist:
                if item.artist_paid:
                    order.artist_paid_amount += item.get_total_price()
                else:
                    order.artist_amount += item.get_total_price()
                    order.fully_paid = False
    return render(request, 'artist/artist_admin.html', {'artist': artist, 'artworks': artworks, 'orders': orders})

@login_required
def add_artwork(request):
    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES)
        if form.is_valid():
            artwork = form.save(commit=False)
            artwork.artist = request.user.artist
            artwork.slug = slugify(artwork.title)
            artwork.save()
            return redirect('artist_admin')
    else:
        form = ArtworkForm()
    return render(request, 'artist/add_artwork.html', {'form': form})

@login_required
def edit_profile(request):
    artist = request.user.artist
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        if name:
            artist.created_by.email = email
            artist.created_by.save()
            artist.name = name
            artist.save()
            return redirect('artist_admin')
    return render(request, 'artist/edit_profile.html', {'artist': artist})

def artists(request):
    artists = Artist.objects.all()
    return render(request, 'artist/artists.html', {'artists': artists})

def artist(request, artist_id):
    artist = get_object_or_404(Artist, pk=artist_id)
    return render(request, 'artist/artist.html', {'artist': artist})