from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Breed(models.Model):

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    size = models.CharField(max_length=20, choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large'), ('extra_large', 'Extra Large')], blank=True)
    temperament = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('breed_detail', kwargs={"pk": self.pk})



class Pet(models.Model):

    PET_STATUS_CHOICES = [
        ('available', 'Available'),
        ('adopted', 'Adopted'),
        ('pending', 'Pending Adoption'),
    ]
    
    name = models.CharField(max_length=100)
    breed = models.ForeignKey(Breed, on_delete=models.PROTECT, related_name='pets')
    age = models.IntegerField(validators=[MinValueValidator(0)])
    description = models.TextField()
    image = models.ImageField(upload_to='pet_images/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=PET_STATUS_CHOICES, default='available')
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('unknown', 'Unknown')], default='unknown')
    health_status = models.TextField(blank=True)
    arrival_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_pets', null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.breed.name})"
    
    def get_absolute_url(self):
        return reverse('pet_detail', kwargs={"pk": self.pk})


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_absolute_url(self):
        return reverse('profile_detail', kwargs={"pk": self.pk})


class AdoptionRequest(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]
    
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='adoption_requests')
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adoption_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    motivation = models.TextField()
    home_type = models.CharField(max_length=100, blank=True)
    has_other_pets = models.BooleanField(default=False)
    other_pets_description = models.TextField(blank=True)
    requested_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('pet', 'requester')
    
    def __str__(self):
        return f"{self.requester.username} - {self.pet.name}"
    
    def get_absolute_url(self):
        return reverse('adoption_request_detail', kwargs={"pk": self.pk})


class Review(models.Model):

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pet_reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Review by {self.author.username} for {self.pet.name}"
    
    def get_absolute_url(self):
        return reverse('review_detail', kwargs={"pk": self.pk})