from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from .forms import AddToCartForm
from .models import Category, Artwork
from apps.cart.cart import Cart

import random


# Create your views here.


def search(request):
    query = request.GET.get('query', '')
    artworks = Artwork.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    return render(request, 'artwork/search.html', {'artworks': artworks, 'query': query})

def artwork(request, category_slug, artwork_slug):
    cart = Cart(request)
    artwork = get_object_or_404(Artwork, category__slug=category_slug, slug=artwork_slug)
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart.add(artwork_id=artwork.id, quantity=quantity, update_quantity=False)
            messages.success(request, 'Artwork was added to the cart')
            return redirect('artwork', category_slug=category_slug, artwork_slug=artwork_slug)
    else:
        form = AddToCartForm()
    similar_artworks = list(artwork.category.artworks.exclude(id=artwork.id))
    if len(similar_artworks) >= 4:
        similar_artworks = random.sample(similar_artworks, 4)
    return render(request, 'artwork/artwork.html', {'form': form, 'artwork': artwork, 'similar_artworks': similar_artworks})

def category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    return render(request, 'artwork/category.html', {'category': category})