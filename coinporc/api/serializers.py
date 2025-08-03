from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import Establishment, EstablishmentImage, Professional, Review, User
from django.contrib.gis.geos import Point

class ProfessionalTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        if user.user_type != 'PRO':
            raise serializers.ValidationError("Authentification réservée aux professionnels")
        
        token = super().get_token(user)
        token['user_type'] = user.user_type
        token['company'] = user.professional.company_name
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)

        # Ajouter les infos de l'utilisateur à la réponse
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'user_type': self.user.user_type,
            'approved':self.user.professional.approved,
            'phone':self.user.phone,
            'company': self.user.professional.company_name if hasattr(self.user, 'professional') else None,
        }

        return data

class ProfessionalRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'phone']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            **validated_data,
            user_type='PRO'
        )
        return user
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    establishment = serializers.PrimaryKeyRelatedField(queryset=Establishment.objects.all())

    class Meta:
        model = Review
        fields = [
            'id', 'user', 'establishment', 'rating', 'comment',
            'pork_quality', 'service_rating', 'photo', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']

        
# --- PROFESSIONAL ---
class ProfessionalSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Professional
        fields = ['id', 'user', 'company_name', 'approved']

# --- ESTABLISHMENT IMAGE ---
class EstablishmentImageSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)

    class Meta:
        model = EstablishmentImage
        fields = ['id', 'establishment', 'image', 'uploaded_by', 'is_approved', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_by', 'is_approved', 'uploaded_at']   

# --- ESTABLISHMENT DETAIL (READ) ---
class EstablishmentDetailSerializer(serializers.ModelSerializer):
    owner = ProfessionalSerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    images = EstablishmentImageSerializer(many=True, read_only=True)
    # promotions = PromotionSerializer(many=True, read_only=True)
    # bookings = BookingSerializer(many=True, read_only=True)
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Establishment
        fields = [
            'id', 'owner', 'name', 'description', 'pork_type', 'location', 'opening_hours', 'is_verified', 'created_at',
            'average_rating', 'reviews', 'images', 'promotions', 'bookings'
        ]


# --- ESTABLISHMENT CREATE / UPDATE ---
class EstablishmentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Establishment
        fields = [
            'id', 'owner', 'name', 'description', 'pork_type', 'location', 'opening_hours',
        ]
        read_only_fields = ['id']

    
    def validate_location(self, value):
        """
        Attend un dict comme : {"type": "Point", "coordinates": [lon, lat]}
        """
        if isinstance(value, dict):
            try:
                lon, lat = value['coordinates']
                return Point(lon, lat)
            except (KeyError, TypeError, ValueError):
                raise serializers.ValidationError("Format de coordonnées invalide.")
        return value