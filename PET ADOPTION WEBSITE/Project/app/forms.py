from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Pet, Breed, UserProfile, AdoptionRequest, Review



class CustomUserCreationForm(UserCreationForm):
    
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def clean_email(self):
 
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
    
    def save(self, commit=True):

        user = super().save(commit=False)
        if commit:
            user.save()
            
            UserProfile.objects.get_or_create(user=user)
        return user



class PetForm(forms.ModelForm):
    
    breed = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Enter breed'}),
        help_text='Type the breed name'
    )
    
    class Meta:
        model = Pet
        fields = ['name', 'age', 'description', 'image', 'gender', 'health_status', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Pet Name'}),
            'age': forms.NumberInput(attrs={'placeholder': 'Age in years'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe the pet'}),
            'image': forms.FileInput(attrs={}),
            'gender': forms.Select(attrs={}),
            'health_status': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Health information'}),
            'status': forms.Select(attrs={}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and hasattr(self.instance, 'breed') and self.instance.breed:
            self.fields['breed'].initial = self.instance.breed.name
    
    def clean_breed(self):
        breed_name = self.cleaned_data.get('breed')
        if not breed_name or not breed_name.strip():
            raise forms.ValidationError("Please enter a breed name.")
        return breed_name.strip()
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        breed_name = self.cleaned_data.get('breed')
        if breed_name:

            breed, _ = Breed.objects.get_or_create(name=breed_name)
            instance.breed = breed
        if commit:
            instance.save()
        return instance

class UserPetForm(forms.ModelForm):
   
    breed = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Enter breed'}),
        help_text='Type the breed name'
    )
    
    class Meta:
        model = Pet
        fields = ['name', 'age', 'description', 'image', 'gender', 'health_status']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Pet Name'}),
            'age': forms.NumberInput(attrs={'placeholder': 'Age in years'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe your pet'}),
            'image': forms.FileInput(attrs={}),
            'gender': forms.Select(attrs={}),
            'health_status': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Health information'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and hasattr(self.instance, 'breed') and self.instance.breed:
            self.fields['breed'].initial = self.instance.breed.name
    
    def clean_breed(self):
        breed_name = self.cleaned_data.get('breed')
        if not breed_name or not breed_name.strip():
            raise forms.ValidationError("Please enter a breed name.")
        return breed_name.strip()
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        breed_name = self.cleaned_data.get('breed')
        if breed_name:
            breed, _ = Breed.objects.get_or_create(name=breed_name)
            instance.breed = breed
        if commit:
            instance.save()
        return instance


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'city', 'state', 'zip_code', 'bio', 'profile_picture']
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'address': forms.TextInput(attrs={'placeholder': 'Street Address'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'placeholder': 'State'}),
            'zip_code': forms.TextInput(attrs={'placeholder': 'ZIP Code'}),
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about yourself'}),
            'profile_picture': forms.FileInput(attrs={}),
        }

class AdoptionRequestForm(forms.ModelForm):
    class Meta:
        model = AdoptionRequest
        fields = ['motivation', 'home_type', 'has_other_pets', 'other_pets_description']
        widgets = {
            'motivation': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Why do you want to adopt this pet?'
            }),
            'home_type': forms.TextInput(attrs={
                'placeholder': 'e.g., House, Apartment'
            }),
            'has_other_pets': forms.CheckboxInput(attrs={}),
            'other_pets_description': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Describe your other pets (if any)'
            }),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'rating', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Review Title'
            }),
            'rating': forms.NumberInput(attrs={
                'min': '1',
                'max': '5',
                'placeholder': 'Rate 1-5'
            }),
            'content': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Share your experience...'
            }),
        }
