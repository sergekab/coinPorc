from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404

from .permissions import IsOwnerProfessional

from .models import Establishment, Professional
from .serializers import EstablishmentDetailSerializer, EstablishmentImageSerializer, EstablishmentWriteSerializer, ProfessionalSerializer, ProfessionalTokenObtainPairSerializer, ProfessionalRegisterSerializer, ReviewSerializer

class ProfessionalLoginView(TokenObtainPairView):
    serializer_class = ProfessionalTokenObtainPairSerializer

class ProfessionalRegisterView(APIView):
    def post(self, request):
        serializer = ProfessionalRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Créez automatiquement le profil pro
            Professional.objects.create(
                user=user,
                company_name=request.data.get('company_name'),
            )
            
            return Response({
                'message': 'Compte professionnel créé. En attente de validation.'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class EstablishmentListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        professional = getattr(request.user, 'professional', None)
        if not professional:
            return Response({'detail': 'Vous n’êtes pas un professionnel.'}, status=403)
        establishments = Establishment.objects.filter(owner=professional)
        serializer = EstablishmentDetailSerializer(establishments, many=True)
        return Response(serializer.data)

    def post(self, request):
        professional = getattr(request.user, 'professional', None)
        if not professional:
            return Response({'detail': 'Vous n’êtes pas un professionnel.'}, status=403)

        # Limite à 5 établissements
        if Establishment.objects.filter(owner=professional).count() >= 5:
            return Response({'detail': 'Vous avez atteint la limite de 5 établissements.'}, status=400)

        data = request.data.copy()
        data['owner'] = professional.id
        serializer = EstablishmentWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

# --- ESTABLISHMENT DETAIL / UPDATE / DELETE ---
class EstablishmentDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerProfessional]

    def get_object(self, pk):
        return get_object_or_404(Establishment, pk=pk)

    def get(self, request, pk):
        establishment = self.get_object(pk)
        serializer = EstablishmentDetailSerializer(establishment)
        return Response(serializer.data)

    def put(self, request, pk):
        establishment = self.get_object(pk)
        serializer = EstablishmentWriteSerializer(establishment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        establishment = self.get_object(pk)
        # Marque comme en attente de suppression
        establishment.pending_deletion = True
        establishment.save()
        return Response({'detail': 'Demande de suppression envoyée à l’administrateur.'}, status=202)
    
class AdminApproveDeleteEstablishmentAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        establishments = Establishment.objects.filter(pending_deletion=True)
        serializer = EstablishmentDetailSerializer(establishments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        establishment = get_object_or_404(Establishment, pk=pk, pending_deletion=True)
        establishment.delete()
        return Response({'detail': 'Établissement supprimé.'}, status=204)
    

class AdminApproveEstablishmentAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def get(self, request):
        establishments = Establishment.objects.filter(is_verified=False)
        serializer = EstablishmentDetailSerializer(establishments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


# --- ADD IMAGE ---
class AddEstablishmentImageAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data['uploaded_by'] = request.user.id
        serializer = EstablishmentImageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AddReviewAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProfessionnalDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk):
        pro = self.get_object(pk)
        serializer = ProfessionalSerializer(pro)
        return Response(serializer.data)