from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.db.models import Q, Avg
from django.http import JsonResponse
from .models import Pet, Breed, UserProfile, AdoptionRequest, Review
from .forms import (PetForm, UserProfileForm, AdoptionRequestForm, 
                    ReviewForm, CustomUserCreationForm, UserPetForm)


class SignUpView(CreateView):

    form_class = CustomUserCreationForm
    template_name = 'app/signup.html'
    success_url = reverse_lazy('login')

class CustomLoginView(LoginView):

    template_name = 'app/login.html'
    success_url = reverse_lazy('home')
    
    def get_success_url(self):
        return reverse_lazy('home')

class CustomLogoutView(TemplateView):

    template_name = 'app/logout.html'
    
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')
    
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')



class HomePageView(TemplateView):

    template_name = 'app/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        context['featured_pets'] = Pet.objects.filter(status='available')[:6]
        
        context['total_pets'] = Pet.objects.filter(status='available').count()
        
        context['total_adoptions'] = AdoptionRequest.objects.filter(status='approved').count()
        return context

class AboutPageView(TemplateView):

    template_name = 'app/about.html'



class PetListView(ListView):
  
    model = Pet
    template_name = 'app/pet_list.html'
    context_object_name = 'pets'
    paginate_by = 12
    
    def get_queryset(self):
       
        queryset = Pet.objects.filter(status='available')
        
        
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | 
                Q(breed__name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
      
        breed = self.request.GET.get('breed')
        if breed:
            queryset = queryset.filter(breed__name__icontains=breed)
        
      
        gender = self.request.GET.get('gender')
        if gender:
            queryset = queryset.filter(gender=gender)
        
       
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        context['breeds'] = Pet.objects.filter(status='available').values_list('breed__name', flat=True).distinct().order_by('breed__name')
        
        context['search_query'] = self.request.GET.get('q', '')
        return context

class PetDetailView(DetailView):
   
    model = Pet
    template_name = 'app/pet_detail.html'
    context_object_name = 'pet'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        context['reviews'] = self.object.reviews.all()
      
        context['average_rating'] = self.object.reviews.aggregate(Avg('rating'))['rating__avg']
        
       
        if self.request.user.is_authenticated:
            
            context['user_adoption_request'] = AdoptionRequest.objects.filter(
                pet=self.object, 
                requester=self.request.user
            ).first()
           
            context['user_review'] = Review.objects.filter(
                pet=self.object,
                author=self.request.user
            ).first()
        
        return context

class PetCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
   
    model = Pet
    form_class = PetForm
    template_name = 'app/pet_form.html'
    
    def test_func(self):
       
        return self.request.user.is_staff

class UserPostPetView(LoginRequiredMixin, CreateView):
   
    model = Pet
    form_class = UserPetForm
    template_name = 'app/user_post_pet.html'
    
    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        
        form.instance.status = 'available'
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_user_post'] = True
        context['breeds'] = Breed.objects.all()
        return context

class PetUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
   
    model = Pet
    form_class = PetForm
    template_name = 'app/pet_form.html'
    
    def test_func(self):
        return self.request.user.is_staff

class UserEditPetView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    
    model = Pet
    form_class = UserPetForm
    template_name = 'app/user_post_pet.html'
    
    def test_func(self):
        pet = self.get_object()
        return pet.posted_by == self.request.user
    
    def handle_no_permission(self):
        return redirect('pet_detail', pk=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_user_post'] = True
        context['is_edit'] = True
        return context

class PetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    
    model = Pet
    template_name = 'app/pet_confirm_delete.html'
    success_url = reverse_lazy('pets')
    
    def test_func(self):
        return self.request.user.is_staff

class UserDeletePetView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
   
    model = Pet
    template_name = 'app/pet_confirm_delete.html'
    success_url = reverse_lazy('my_pets')
    
    def test_func(self):
        pet = self.get_object()
        return pet.posted_by == self.request.user
    
    def handle_no_permission(self):
        return redirect('pet_detail', pk=self.kwargs['pk'])

class MyPetsView(LoginRequiredMixin, ListView):
   
    model = Pet
    template_name = 'app/my_pets.html'
    context_object_name = 'pets'
    paginate_by = 12
    
    def get_queryset(self):
        return Pet.objects.filter(posted_by=self.request.user).order_by('-created_at')



class ProfileDetailView(DetailView):
    
    model = UserProfile
    template_name = 'app/profile_detail.html'
    context_object_name = 'profile'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['adoption_requests'] = AdoptionRequest.objects.filter(
            requester=self.object.user
        )
        context['reviews'] = Review.objects.filter(author=self.object.user)
        return context

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'app/profile_form.html'
    
    def get_object(self):
        return self.request.user.profile
    
    def get_success_url(self):
        return reverse_lazy('profile_detail', kwargs={'pk': self.object.pk})

class UserProfileListView(ListView):
   
    model = UserProfile
    template_name = 'app/profile_list.html'
    context_object_name = 'profiles'
    paginate_by = 12



class AdoptionRequestListView(LoginRequiredMixin, ListView):
    
    model = AdoptionRequest
    template_name = 'app/adoption_request_list.html'
    context_object_name = 'requests'
    paginate_by = 12
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return AdoptionRequest.objects.all()
        return AdoptionRequest.objects.filter(requester=self.request.user)

class AdoptionRequestDetailView(LoginRequiredMixin, DetailView):
    
    model = AdoptionRequest
    template_name = 'app/adoption_request_detail.html'
    context_object_name = 'adoption_request'
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return AdoptionRequest.objects.all()
        return AdoptionRequest.objects.filter(requester=self.request.user)

class AdoptionRequestCreateView(LoginRequiredMixin, CreateView):
    
    model = AdoptionRequest
    form_class = AdoptionRequestForm
    template_name = 'app/adoption_request_form.html'
    
    def form_valid(self, form):
        form.instance.requester = self.request.user
        pet_id = self.kwargs.get('pet_id')
        form.instance.pet = Pet.objects.get(pk=pet_id)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('pet_detail', kwargs={'pk': self.object.pet.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pet_id = self.kwargs.get('pet_id')
        context['pet'] = Pet.objects.get(pk=pet_id)
        return context

class AdoptionRequestUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    
    model = AdoptionRequest
    form_class = AdoptionRequestForm
    template_name = 'app/adoption_request_form.html'
    
    def test_func(self):
        return (self.request.user == self.get_object().requester or 
                self.request.user.is_staff)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pet'] = self.get_object().pet
        return context
    
    def get_success_url(self):
        return reverse_lazy('pet_detail', kwargs={'pk': self.object.pet.pk})

class AdoptionRequestDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
   
    model = AdoptionRequest
    template_name = 'app/adoption_request_confirm_delete.html'
    success_url = reverse_lazy('adoption_requests')
    
    def test_func(self):
        return (self.request.user == self.get_object().requester or 
                self.request.user.is_staff)

class AdoptionRequestApproveView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = AdoptionRequest
    fields = []
    template_name = 'app/adoption_request_approve.html'
    
    def test_func(self):
        return self.request.user.is_staff
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.status == 'pending':
            self.object.status = 'approved'
            pet = self.object.pet
            pet.status = 'adopted'
            pet.save()
            self.object.save()
            messages.success(request, f"Adoption request for {pet.name} has been approved!")
        return redirect('adoption_request_detail', pk=self.object.pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['adoption_request'] = self.object
        return context



class ReviewListView(ListView):
    model = Review
    template_name = 'app/review_list.html'
    context_object_name = 'reviews'
    paginate_by = 12
    
    def get_queryset(self):
        return Review.objects.all().order_by('-created_at')

class ReviewDetailView(DetailView):
    model = Review
    template_name = 'app/review_detail.html'
    context_object_name = 'review'

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'app/review_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        pet_id = self.kwargs.get('pet_id')
        form.instance.pet = Pet.objects.get(pk=pet_id)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('pet_detail', kwargs={'pk': self.object.pet.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pet_id = self.kwargs.get('pet_id')
        context['pet'] = Pet.objects.get(pk=pet_id)
        return context

class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'app/review_form.html'
    
    def test_func(self):
        return (self.request.user == self.get_object().author or 
                self.request.user.is_staff)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pet'] = self.get_object().pet
        return context
    
    def get_success_url(self):
        return reverse_lazy('pet_detail', kwargs={'pk': self.object.pet.pk})

class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'app/review_confirm_delete.html'
    
    def test_func(self):
        return (self.request.user == self.get_object().author or 
                self.request.user.is_staff)
    
    def get_success_url(self):
        return reverse_lazy('pet_detail', kwargs={'pk': self.object.pet.pk})


class PetSearchAPIView(ListView):
    model = Pet
    template_name = 'app/pet_list.html'
    context_object_name = 'pets'
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        return Pet.objects.filter(
            Q(name__icontains=query) | 
            Q(breed__name__icontains=query) |
            Q(description__icontains=query)
        )
    
    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            pets = list(self.get_queryset().values('id', 'name', 'breed__name', 'image'))
            return JsonResponse({'pets': pets})
        return super().render_to_response(context, **response_kwargs)

class MyPetsView(LoginRequiredMixin, ListView):
    """Show all pets posted by the current user"""
    model = Pet
    template_name = 'app/my_pets.html'
    context_object_name = 'pets'
    paginate_by = 12
    
    def get_queryset(self):
        return Pet.objects.filter(posted_by=self.request.user).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posted_pets = Pet.objects.filter(posted_by=self.request.user)
        context['total_posted'] = posted_pets.count()
        context['total_adopted'] = posted_pets.filter(status='adopted').count()
        

        adopted_pets_ids = AdoptionRequest.objects.filter(
            requester=self.request.user, 
            status='approved'
        ).values_list('pet_id', flat=True)
        context['adopted_pets'] = Pet.objects.filter(pk__in=adopted_pets_ids).order_by('-updated_at')
        context['total_my_adoptions'] = context['adopted_pets'].count()
        
        return context




class PetListAPIView(ListView):
    model = Pet
    
    def get_queryset(self):
        status = self.request.GET.get('status', 'available')
        gender = self.request.GET.get('gender')
        breed_id = self.request.GET.get('breed_id')
        search = self.request.GET.get('search')
        
        pets = Pet.objects.select_related('breed').filter(status=status)
        
        if gender:
            pets = pets.filter(gender=gender)
        
        if breed_id:
            try:
                pets = pets.filter(breed_id=int(breed_id))
            except (ValueError, TypeError):
                pass
        
        if search:
            pets = pets.filter(
                Q(name__icontains=search) |
                Q(breed__name__icontains=search) |
                Q(description__icontains=search)
            )
        
        return pets.order_by('-created_at')
    
    def render_to_response(self, context, **response_kwargs):
        pets = list(self.get_queryset().values(
            'id', 'name', 'breed__name', 'breed__id', 'age', 'gender',
            'status', 'image', 'description', 'health_status', 'created_at'
        ))
        
        pets_data = []
        for pet in pets:
            pets_data.append({
                'id': pet['id'],
                'name': pet['name'],
                'breed': pet['breed__name'],
                'breed_id': pet['breed__id'],
                'age': pet['age'],
                'gender': pet['gender'],
                'status': pet['status'],
                'image': pet['image'],
                'description': pet['description'],
                'health_status': pet['health_status'],
                'created_at': str(pet['created_at']),
            })
        
        return JsonResponse({
            'count': len(pets_data),
            'results': pets_data,
            'status': 'success'
        })


class PetDetailAPIView(DetailView):
    model = Pet
    pk_url_kwarg = 'pet_id'
    
    def render_to_response(self, context, **response_kwargs):
        pet = self.get_object()
        
        adoption_requests = AdoptionRequest.objects.filter(pet=pet)
        approved_count = adoption_requests.filter(status='approved').count()
        pending_count = adoption_requests.filter(status='pending').count()
        
        reviews = Review.objects.filter(pet=pet)
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        
        pet_data = {
            'id': pet.id,
            'name': pet.name,
            'breed': pet.breed.name,
            'breed_id': pet.breed.id,
            'breed_info': {
                'id': pet.breed.id,
                'name': pet.breed.name,
                'size': pet.breed.size,
                'temperament': pet.breed.temperament,
                'description': pet.breed.description,
            },
            'age': pet.age,
            'gender': pet.gender,
            'status': pet.status,
            'image': pet.image.url if pet.image else None,
            'description': pet.description,
            'health_status': pet.health_status,
            'arrival_date': str(pet.arrival_date),
            'created_at': str(pet.created_at),
            'updated_at': str(pet.updated_at),
            'posted_by': {
                'id': pet.posted_by.id,
                'username': pet.posted_by.username,
                'profile_url': f'/profiles/{pet.posted_by.profile.id}/'
            } if pet.posted_by else None,
            'adoption_stats': {
                'total_requests': adoption_requests.count(),
                'approved_count': approved_count,
                'pending_count': pending_count,
            },
            'reviews': {
                'count': reviews.count(),
                'average_rating': round(avg_rating, 2) if avg_rating else None,
            }
        }
        
        return JsonResponse({
            'status': 'success',
            'data': pet_data
        })


class BreedListAPIView(ListView):
    model = Breed
    
    def get_queryset(self):
        return Breed.objects.all().order_by('name')
    
    def render_to_response(self, context, **response_kwargs):
        breeds = self.get_queryset()
        
        breeds_data = []
        for breed in breeds:
            pet_count = Pet.objects.filter(breed=breed, status='available').count()
            breeds_data.append({
                'id': breed.id,
                'name': breed.name,
                'size': breed.size,
                'temperament': breed.temperament,
                'description': breed.description,
                'available_pets': pet_count,
                'created_at': str(breed.created_at),
            })
        
        return JsonResponse({
            'count': len(breeds_data),
            'results': breeds_data,
            'status': 'success'
        })
