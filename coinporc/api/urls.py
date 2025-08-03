from django.urls import path
from .views import AddEstablishmentImageAPIView, AddReviewAPIView, EstablishmentDetailAPIView, EstablishmentListCreateAPIView, ProfessionalLoginView, ProfessionalRegisterView, ProfessionnalDetailAPIView

urlpatterns = [
    path('login/', ProfessionalLoginView.as_view(), name='pro-login'),
    path('register/', ProfessionalRegisterView.as_view(), name='pro-register'),
    path('establishments/', EstablishmentListCreateAPIView.as_view(), name='establishment-list-create'),
    path('establishments/<int:pk>/', EstablishmentDetailAPIView.as_view(), name='establishment-detail'),
    path('reviews/', AddReviewAPIView.as_view(), name='add-review'),
    path('images/', AddEstablishmentImageAPIView.as_view(), name='add-image'),
    path('me/<int:pk>/', ProfessionnalDetailAPIView.as_view(), name='user-detail'),
]