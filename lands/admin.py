from django.contrib import admin
from .models import LandCategory, Land, LandImage, LandDocument, Inquiry, Favorite

class LandImageInline(admin.TabularInline):
    model = LandImage
    extra = 1

class LandDocumentInline(admin.TabularInline):
    model = LandDocument
    extra = 1

@admin.register(LandCategory)
class LandCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Land)
class LandAdmin(admin.ModelAdmin):
    list_display = ['title', 'seller', 'price', 'area', 'city', 'land_type', 'status', 'featured', 'created_at']
    list_filter = ['status', 'land_type', 'featured', 'created_at']
    search_fields = ['title', 'description', 'location', 'city']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [LandImageInline, LandDocumentInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'seller', 'category')
        }),
        ('Pricing & Area', {
            'fields': ('price', 'area')
        }),
        ('Location', {
            'fields': ('location', 'city', 'state', 'pincode', 'latitude', 'longitude')
        }),
        ('Type & Status', {
            'fields': ('land_type', 'status', 'featured')
        }),
    )

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['land', 'name', 'email', 'phone', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'land__title']
    readonly_fields = ['created_at']

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'land', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'land__title']