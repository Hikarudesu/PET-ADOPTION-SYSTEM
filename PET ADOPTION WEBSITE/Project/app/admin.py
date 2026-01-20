from django.contrib import admin
from .models import Breed, Pet, UserProfile, AdoptionRequest, Review

@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ['name', 'size', 'created_at']
    list_filter = ['size', 'created_at']
    search_fields = ['name', 'temperament']
    readonly_fields = ['created_at']

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ['name', 'breed', 'age', 'status', 'gender', 'created_at']
    list_filter = ['status', 'gender', 'breed', 'created_at']
    search_fields = ['name', 'breed__name']
    readonly_fields = ['created_at', 'updated_at', 'arrival_date']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'is_verified', 'created_at']
    list_filter = ['is_verified', 'created_at']
    search_fields = ['user__username', 'city']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ['requester', 'pet', 'status', 'requested_date']
    list_filter = ['status', 'requested_date']
    search_fields = ['requester__username', 'pet__name']
    readonly_fields = ['requested_date', 'updated_date']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['author', 'pet', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['author__username', 'pet__name', 'title']
    readonly_fields = ['created_at', 'updated_at']

