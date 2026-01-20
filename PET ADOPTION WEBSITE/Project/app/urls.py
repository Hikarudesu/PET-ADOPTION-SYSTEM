from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    HomePageView, AboutPageView,
    PetListView, PetDetailView, PetCreateView, PetUpdateView, PetDeleteView, PetSearchAPIView,
    UserPostPetView, UserEditPetView, UserDeletePetView, MyPetsView,
    AdoptionRequestListView, AdoptionRequestDetailView, AdoptionRequestCreateView, 
    AdoptionRequestUpdateView, AdoptionRequestDeleteView, AdoptionRequestApproveView,
    ReviewListView, ReviewDetailView, ReviewCreateView, ReviewUpdateView, ReviewDeleteView,
    ProfileDetailView, ProfileUpdateView, UserProfileListView,
    SignUpView, CustomLoginView, CustomLogoutView,
    PetListAPIView, PetDetailAPIView, BreedListAPIView
)

urlpatterns = [

    path('', HomePageView.as_view(), name='home'),
    
    
    path('about/', AboutPageView.as_view(), name='about'),
    
   
    path('signup/', SignUpView.as_view(), name='signup'),
    
   
    path('login/', CustomLoginView.as_view(), name='login'),
    
   
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    
   
    path('pets/', PetListView.as_view(), name='pets'),
    
    
    path('pets/<int:pk>/', PetDetailView.as_view(), name='pet_detail'),
    
   
    path('pets/create/', PetCreateView.as_view(), name='pet_create'),
    
   
    path('pets/<int:pk>/edit/', PetUpdateView.as_view(), name='pet_update'),
    
   
    path('pets/<int:pk>/delete/', PetDeleteView.as_view(), name='pet_delete'),
    
   
    path('pets/search/', PetSearchAPIView.as_view(), name='pet_search'),
    
   
    path('my-pets/', MyPetsView.as_view(), name='my_pets'),
 
    path('post-pet/', UserPostPetView.as_view(), name='post_pet'),
    
   
    path('my-pets/<int:pk>/edit/', UserEditPetView.as_view(), name='user_edit_pet'),
    
  
    path('my-pets/<int:pk>/delete/', UserDeletePetView.as_view(), name='user_delete_pet'),
    
   
    path('adoption-requests/', AdoptionRequestListView.as_view(), name='adoption_requests'),
    
    
    path('adoption-requests/<int:pk>/', AdoptionRequestDetailView.as_view(), name='adoption_request_detail'),
    
   
    path('pets/<int:pet_id>/adopt/', AdoptionRequestCreateView.as_view(), name='adoption_request_create'),
    
    
    path('adoption-requests/<int:pk>/edit/', AdoptionRequestUpdateView.as_view(), name='adoption_request_update'),
    
   
    path('adoption-requests/<int:pk>/delete/', AdoptionRequestDeleteView.as_view(), name='adoption_request_delete'),
    
  
    path('adoption-requests/<int:pk>/approve/', AdoptionRequestApproveView.as_view(), name='adoption_request_approve'),
    
    
    path('reviews/', ReviewListView.as_view(), name='reviews'),
    
    
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review_detail'),
    
   
    path('pets/<int:pet_id>/review/', ReviewCreateView.as_view(), name='review_create'),
    
    
    path('reviews/<int:pk>/edit/', ReviewUpdateView.as_view(), name='review_update'),
    
   
    path('reviews/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review_delete'),
    
    
    path('profiles/', UserProfileListView.as_view(), name='profiles'),
    
   
    path('profiles/<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    
   
    path('profiles/edit/', ProfileUpdateView.as_view(), name='profile_update'),
    
   
    path('api/pets/', PetListAPIView.as_view(), name='api_pet_list'),
    
   
    path('api/pets/<int:pet_id>/', PetDetailAPIView.as_view(), name='api_pet_detail'),
    
   
    path('api/breeds/', BreedListAPIView.as_view(), name='api_breed_list'),
]