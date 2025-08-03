from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Professional, Establishment, Review, Promotion, Booking, EstablishmentImage

# Customisation de l'affichage du User dans l'admin
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_staff', 'email_verified')
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'phone')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'email', 'phone', 'profile_pic', 'favorites')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Type utilisateur', {'fields': ('user_type', 'email_verified')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )
    filter_horizontal = ('groups', 'user_permissions', 'favorites')

admin.site.register(User, UserAdmin)

@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'approved')
    list_filter = ('approved',)
    search_fields = ('company_name', 'user__email')

@admin.register(Establishment)
class EstablishmentAdmin(admin.ModelAdmin):
    list_display = ('name','owner', 'pork_type','is_verified')
    list_filter = ('pork_type', 'is_verified')
    search_fields = ('name', 'owner__company_name')
    autocomplete_fields = ['owner']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'establishment', 'rating', 'pork_quality', 'service_rating', 'created_at')
    list_filter = ('rating', 'pork_quality', 'service_rating')
    search_fields = ('user__username', 'establishment__name')

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('title', 'establishment', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'establishment__name')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'establishment', 'date', 'guests', 'created_at')
    list_filter = ('date',)
    search_fields = ('user__username', 'establishment__name')

@admin.register(EstablishmentImage)
class EstablishmentImageAdmin(admin.ModelAdmin):
    list_display = ('establishment', 'uploaded_by', 'is_approved', 'uploaded_at')
    list_filter = ('is_approved',)
    search_fields = ('establishment__name', 'uploaded_by__username')

