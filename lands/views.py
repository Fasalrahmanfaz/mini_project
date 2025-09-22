# File: C:\Users\91999\Desktop\Fasal Documents\landmarket\lands\views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils.text import slugify
from .models import Land, LandImage, Inquiry, Favorite, LandCategory
from .forms import LandForm, LandImageForm, InquiryForm, LandSearchForm

def home(request):
    featured_lands = Land.objects.filter(featured=True, status='available')[:6]
    recent_lands = Land.objects.filter(status='available')[:8]
    categories = LandCategory.objects.all()
    
    context = {
        'featured_lands': featured_lands,
        'recent_lands': recent_lands,
        'categories': categories,
    }
    return render(request, 'lands/home.html', context)

def land_list(request):
    lands = Land.objects.filter(status='available')
    form = LandSearchForm(request.GET)
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        land_type = form.cleaned_data.get('land_type')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        min_area = form.cleaned_data.get('min_area')
        max_area = form.cleaned_data.get('max_area')
        
        if query:
            lands = lands.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(location__icontains=query) |
                Q(city__icontains=query)
            )
        
        if land_type:
            lands = lands.filter(land_type=land_type)
        
        if min_price:
            lands = lands.filter(price__gte=min_price)
        
        if max_price:
            lands = lands.filter(price__lte=max_price)
        
        if min_area:
            lands = lands.filter(area__gte=min_area)
        
        if max_area:
            lands = lands.filter(area__lte=max_area)
    
    paginator = Paginator(lands, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'form': form,
        'total_count': lands.count(),
    }
    return render(request, 'lands/land_list.html', context)

def land_detail(request, slug):
    land = get_object_or_404(Land, slug=slug)
    related_lands = Land.objects.filter(
        land_type=land.land_type,
        status='available'
    ).exclude(id=land.id)[:4]
    
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, land=land).exists()
    
    context = {
        'land': land,
        'related_lands': related_lands,
        'is_favorite': is_favorite,
    }
    return render(request, 'lands/land_detail.html', context)

@login_required
def add_land(request):
    if request.method == 'POST':
        form = LandForm(request.POST)
        if form.is_valid():
            land = form.save(commit=False)
            land.seller = request.user
            land.slug = slugify(land.title)
            
            # Handle duplicate slugs
            original_slug = land.slug
            counter = 1
            while Land.objects.filter(slug=land.slug).exists():
                land.slug = f"{original_slug}-{counter}"
                counter += 1
            
            land.save()
            
            # Handle multiple image uploads
            images = request.FILES.getlist('images')
            for i, image in enumerate(images):
                LandImage.objects.create(
                    land=land,
                    image=image,
                    is_primary=(i == 0)  # First image is primary
                )
            
            messages.success(request, 'Land listing created successfully!')
            return redirect('land_detail', slug=land.slug)
    else:
        form = LandForm()
    
    return render(request, 'lands/add_land.html', {'form': form})

@login_required
def edit_land(request, slug):
    land = get_object_or_404(Land, slug=slug, seller=request.user)
    
    if request.method == 'POST':
        form = LandForm(request.POST, instance=land)
        if form.is_valid():
            form.save()
            
            # Handle new image uploads
            images = request.FILES.getlist('images')
            for image in images:
                LandImage.objects.create(land=land, image=image)
            
            messages.success(request, 'Land listing updated successfully!')
            return redirect('land_detail', slug=land.slug)
    else:
        form = LandForm(instance=land)
    
    return render(request, 'lands/edit_land.html', {'form': form, 'land': land})

@login_required
def delete_land(request, slug):
    land = get_object_or_404(Land, slug=slug, seller=request.user)
    
    if request.method == 'POST':
        land.delete()
        messages.success(request, 'Land listing deleted successfully!')
        return redirect('my_listings')
    
    return render(request, 'lands/delete_land.html', {'land': land})

@login_required
def my_listings(request):
    lands = Land.objects.filter(seller=request.user)
    return render(request, 'lands/my_listings.html', {'lands': lands})

def inquiry(request, slug):
    land = get_object_or_404(Land, slug=slug)
    
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.land = land
            if request.user.is_authenticated:
                inquiry.user = request.user
            inquiry.save()
            
            messages.success(request, 'Your inquiry has been sent successfully!')
            return redirect('land_detail', slug=land.slug)
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'name': request.user.get_full_name() or request.user.username,
                'email': request.user.email,
            }
        form = InquiryForm(initial=initial_data)
    
    return render(request, 'lands/inquiry.html', {'form': form, 'land': land})

@login_required
def toggle_favorite(request, slug):
    land = get_object_or_404(Land, slug=slug)
    favorite, created = Favorite.objects.get_or_create(user=request.user, land=land)
    
    if not created:
        favorite.delete()
        messages.success(request, 'Removed from favorites!')
    else:
        messages.success(request, 'Added to favorites!')
    
    return redirect('land_detail', slug=land.slug)

@login_required
def my_favorites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('land')
    return render(request, 'lands/my_favorites.html', {'favorites': favorites})

@login_required
def my_inquiries(request):
    # For sellers - show inquiries on their lands
    inquiries = Inquiry.objects.filter(land__seller=request.user).order_by('-created_at')
    return render(request, 'lands/my_inquiries.html', {'inquiries': inquiries})

def about(request):
    return render(request, 'lands/about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # In a real app, you would send an email here
        # For now, we'll just show a success message
        messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
        return redirect('contact')
    
    return render(request, 'lands/contact.html')